# SmartSorter‑PC

A lightweight, cross-platform daemon + UI tool that watches "incoming" folders (Downloads, Desktop, etc.) on your PC, auto-sorts files with high confidence, and surfaces ambiguous files for quick manual review. Designed for speed, accuracy, and seamless integration.

---

## 🧠 1. Overview

**Tool Name:** `SmartSorter‑PC`
**Target Platforms:** Windows, macOS, Linux

**Key Idea:**
An always-on desktop assistant that classifies and organizes files using rule-based logic and ML fallback, allowing one-click sorting for low-confidence items via an intuitive UI.

**Top-Level Components:**

1. **Watcher Daemon** — monitors folders in real-time
2. **Processing Pipeline** — combines rule engine, ML classifier, vector model
3. **Local Storage** — includes SQLite, FAISS, ONNX model files
4. **UI App** — built with Electron, cross-platform
5. **Trainer Subsystem** — handles online learning & feedback integration

---

## ⚙️ 2. Core Functionalities

1. **Realtime File Monitoring**
2. **Instant Rule-Based Sorting**
3. **ML-Driven Sorting**

   * Supervised classifier
   * Vector similarity fallback
4. **Undo + Pending Review UI**
5. **Feedback Loop & Online Retraining**
6. **Notifications & Shell Integration** (optional)

---

## 📋 3. Requirements

### 3.1 Non-Functional

| Property         | Target                                |
| ---------------- | ------------------------------------- |
| Latency          | ≤ 100 ms end-to-end per file          |
| Memory Footprint | ≤ 200 MB resident memory              |
| Startup Time     | < 2 s for daemon + UI                 |
| Reliability      | 99.9% uptime, ACID for pending queue  |
| Portability      | Windows 10+, macOS 11+, Ubuntu 20.04+ |

### 3.2 Functional

| Feature                    | Implementation Details                                                           |
| -------------------------- | -------------------------------------------------------------------------------- |
| File Monitoring            | FS watcher (debounced, deduped); cross-platform                                  |
| Rule-Based Sorting         | In-memory mapping (ext → folder); JSON config w/ hot reload                      |
| ML Classification          | TF-IDF + LogisticRegression (ONNX); confidence threshold, supports `partial_fit` |
| Vector Similarity Sorting  | ONNX embedder (MiniLM) → FAISS centroid lookup                                   |
| Pending Review UI          | List view (filename, preview, top-3 predictions, drag/drop support)              |
| Undo & Notifications       | Native toast APIs; undo token (10s TTL) routed back to daemon                    |
| Feedback & Retraining      | Buffered learning; periodic `partial_fit`; model persistence                     |
| Storage                    | SQLite + FTS5; ONNX, vocab, FAISS stored locally; config in YAML/JSON            |
| Installation & Integration | Platform installers (MSI, .dmg, .deb); optional shell context menu               |

---

## 🧩 4. Mechanism-to-Requirement Map

| Requirement              | Mechanism                                        |
| ------------------------ | ------------------------------------------------ |
| Cross-platform FS events | `watchdog` (Python) or `chokidar` (Node.js)      |
| Rule-based mapping       | In-memory JSON rule engine                       |
| ML classification        | ONNX LogisticRegression, supports `partial_fit`  |
| Semantic fallback        | SentenceTransformer ONNX → FAISS centroid lookup |
| Pending review           | Confidence threshold → deferred UI handoff       |
| Real-time UI feedback    | Electron IPC (WebSocket/gRPC)                    |
| Undo support             | In-process stack + notification callback         |
| Continuous learning      | Threaded trainer with `joblib` + ONNX export     |
| Data querying            | SQLite + FTS5, FAISS index (memory-mapped)       |

---

## 🧱 5. Code Specs

### 5.1 Project Structure

```
smartsorter-pc/
├── daemon/
│   ├── watcher.py            # Filesystem events + debounce
│   ├── pipeline/             # rules.py, classifier.py, vector.py
│   ├── store.py              # DB, FAISS, model accessors
│   ├── trainer.py            # Feedback handler & retraining loop
│   └── notifier.py           # Toasts + undo API
├── ui/
│   ├── src/                  # Electron + React frontend
│   └── ipc/                  # WebSocket/gRPC stubs
├── models/
│   ├── rules.json  
│   ├── tfidf_vocab.pkl  
│   ├── classifier.onnx  
│   ├── embedder.onnx  
│   └── faiss_index.faiss  
├── config/
│   └── settings.yaml         # Configs: thresholds, watched paths, DB paths
├── scripts/                  # Installer builders, shell extension
└── tests/                    # Unit + integration tests
```

### 5.2 Key Modules & Interfaces

#### `watcher.py`

```python
class FileWatcher:
    def __init__(self, paths: List[Path], event_queue: EventQueue, debounce_ms: int = 500): ...
    def start(self) -> None: ...
    def stop(self) -> None: ...
```

#### `rules.py`

```python
class RuleEngine:
    def __init__(self, rules: Dict[str, Path]): ...
    def match(self, filepath: Path) -> Optional[Path]: ...
    def reload_rules(self) -> None  # Hot-reload from JSON
```

#### `classifier.py`

```python
class ClassifierEngine:
    def __init__(self, model_path: Path, vocab_path: Path, threshold: float): ...
    def featurize(self, filepath: Path) -> np.ndarray: ...
    def predict(self, features: np.ndarray) -> Tuple[Path, float]: ...
    def partial_fit(self, features: np.ndarray, target_folder: Path) -> None: ...
```

#### `vector.py`

```python
class VectorEngine:
    def __init__(self, model_path: Path, index_path: Path, threshold: float): ...
    def embed(self, filepath: Path) -> np.ndarray: ...
    def nearest_folder(self, embedding: np.ndarray) -> Tuple[Path, float]: ...
    def recompute_centroid(self, folder: Path) -> None: ...
```

#### `store.py`

```python
class PersistentStore:
    def __init__(self, db_path: Path, faiss_index_path: Path): ...
    def enqueue_pending(self, filepath: Path, suggestions: List[Tuple[Path, float]]): ...
    def dequeue_feedback(self) -> List[FeedbackItem]: ...
    def save_model(self, engine_name: str, artifact_path: Path) -> None: ...
```

#### `trainer.py`

```python
class Trainer:
    def __init__(self, store: PersistentStore, classifier: ClassifierEngine, interval_secs: int): ...
    def run(self) -> None  # Loop: sleep → collect feedback → partial_fit → persist
```

### 5.3 Performance Targets & Deployment

**Benchmarks (via `pytest-benchmark`)**

* `rules.match()` → < 0.5 ms
* `classifier.predict()` → < 2 ms
* `vector.embed()` + `nearest_folder()` → < 50 ms

**Packaging & Deployment**

* Daemon registered as background service
* UI bundled with `electron-builder` (native installer per OS)
* Shell extension boilerplate generated via SDK tooling or Yeoman
