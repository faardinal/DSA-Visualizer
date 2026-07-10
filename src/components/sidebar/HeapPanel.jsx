import { memo } from "react";
import { Database } from "lucide-react";

const SKIP_TYPES = new Set(["function", "unsupported", "module", "type"]);

function HeapPanel({ snapshot, events }) {
  const heap = (snapshot?.heap || []).filter((o) => !SKIP_TYPES.has(o.type));

  return (
    <div className="px-4 py-3 h-full overflow-y-auto">
      <div className="flex items-center gap-1.5 mb-2">
        <Database className="w-3 h-3 text-muted-foreground/60" />
        <span className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground/60">
          Heap Objects
        </span>
        <span className="ml-auto text-[10px] font-mono text-muted-foreground/40">{heap.length}</span>
      </div>
      {heap.length === 0 ? (
        <p className="text-[11px] text-muted-foreground/50 italic">No heap objects</p>
      ) : (
        <div className="flex flex-col gap-3">
          {heap.map((obj) => (
            <HeapEntry key={obj.id} obj={obj} events={events} />
          ))}
        </div>
      )}
    </div>
  );
}

function HeapEntry({ obj, events }) {
  const hasChange = (events || []).some(
    (e) => String(e.objectId) === String(obj.id) && e.type !== "Highlight"
  );

  return (
    <div
      className={`rounded-md border transition-colors duration-500 overflow-hidden ${
        hasChange ? "border-primary/50 bg-primary/5" : "border-border"
      }`}
    >
      <div className="px-2 py-1 bg-muted/30 flex items-center gap-1.5">
        <span className="text-[9px] font-mono text-muted-foreground/50">{obj.id}</span>
        <span className="text-[9px] font-semibold text-primary/60 uppercase ml-auto">{obj.type}</span>
      </div>
      <div className="p-2 text-xs font-mono overflow-x-auto max-h-32 overflow-y-auto">
        <HeapObjectInline obj={obj} />
      </div>
    </div>
  );
}

function HeapObjectInline({ obj }) {
  const { type, value } = obj;
  if (type === "list" || type === "tuple" || type === "array") {
    const arr = Array.isArray(value) ? value : [];
    return (
      <span className="text-foreground/80">
        [{arr.map((v, i) => (
          <span key={i}>
            {i > 0 && <span className="text-muted-foreground">, </span>}
            <ValueDisplay v={v} />
          </span>
        ))}]
      </span>
    );
  }
  if (type === "set") {
    const arr = Array.isArray(value) ? value : [];
    return (
      <span className="text-foreground/80">
        {"{"}
        {arr.map((v, i) => (
          <span key={i}>
            {i > 0 && <span className="text-muted-foreground">, </span>}
            <ValueDisplay v={v} />
          </span>
        ))}
        {"}"}
      </span>
    );
  }
  if (type === "dict") {
    const entries = Object.entries(value || {});
    return (
      <span className="text-foreground/80">
        {"{"}
        {entries.map(([k, v], i) => (
          <span key={k}>
            {i > 0 && <span className="text-muted-foreground">, </span>}
            <span className="text-primary/70">{k}</span>
            <span className="text-muted-foreground">: </span>
            <ValueDisplay v={v} />
          </span>
        ))}
        {"}"}
      </span>
    );
  }
  if (type === "linkedlist") {
    const chain = Array.isArray(value) ? value : [];
    return (
      <span className="text-foreground/80">
        {chain.map((n, i) => (
          <span key={n.id ?? i}>
            {i > 0 && <span className="text-muted-foreground"> → </span>}
            <span>{String(n.value)}</span>
          </span>
        ))}
      </span>
    );
  }
  if (type === "tree") {
    return <span className="text-muted-foreground/60 italic">Tree (see canvas)</span>;
  }
  // Custom object / fallback
  const attrs = value && typeof value === "object" ? Object.entries(value) : [];
  if (attrs.length > 0) {
    return (
      <span className="text-foreground/80">
        {"{"}
        {attrs.map(([k, v], i) => (
          <span key={k}>
            {i > 0 && <span className="text-muted-foreground">, </span>}
            <span className="text-primary/70">{k}</span>
            <span className="text-muted-foreground">: </span>
            <ValueDisplay v={v} />
          </span>
        ))}
        {"}"}
      </span>
    );
  }
  return <span className="text-muted-foreground/60 italic">{type}</span>;
}

function ValueDisplay({ v }) {
  if (v === null) return <span className="text-muted-foreground/60">null</span>;
  if (typeof v === "object" && "ref" in v) {
    return <span className="text-primary/60 cursor-pointer">{`→${v.ref}`}</span>;
  }
  if (typeof v === "string") return <span className="text-emerald-600/80">"{v}"</span>;
  return <span className="text-foreground/80">{String(v)}</span>;
}

export default memo(HeapPanel);
