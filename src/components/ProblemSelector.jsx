/**
 * ProblemSelector.jsx
 * Dropdown for selecting a problem when method name is ambiguous,
 * or for explicitly choosing a problem before running.
 */
import { memo, useState, useEffect } from 'react';
import { ChevronDown, Search } from 'lucide-react';
import { fetchProblems } from '@/lib/runSolution';

const DIFF_COLORS = {
  Easy: 'text-emerald-500 bg-emerald-500/10',
  Medium: 'text-amber-500 bg-amber-500/10',
  Hard: 'text-destructive bg-destructive/10',
};

function ProblemSelector({ selectedId, onSelect, className = '' }) {
  const [problems, setProblems] = useState([]);
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');

  useEffect(() => {
    fetchProblems().then(setProblems).catch(() => {});
  }, []);

  const selected = problems.find((p) => p.problem_id === selectedId);
  const filtered = problems.filter((p) => {
    if (!query) return true;
    const q = query.toLowerCase();
    return p.title.toLowerCase().includes(q)
      || p.method_name.toLowerCase().includes(q)
      || p.pattern.toLowerCase().includes(q);
  });

  return (
    <div className={`relative ${className}`}>
      <button
        onClick={() => setOpen((o) => !o)}
        className="flex items-center gap-1.5 px-2 py-1 rounded text-[11px] bg-muted/50 hover:bg-muted text-foreground border border-border"
      >
        <span className="truncate max-w-[140px]">
          {selected ? selected.title : 'Select problem'}
        </span>
        <ChevronDown className="w-3 h-3 text-muted-foreground" />
      </button>

      {open && (
        <>
          <div className="fixed inset-0 z-40" onClick={() => setOpen(false)} />
          <div className="absolute z-50 mt-1 w-72 max-h-80 flex flex-col bg-popover border border-border rounded-md shadow-lg overflow-hidden">
            <div className="p-2 border-b border-border flex items-center gap-1.5">
              <Search className="w-3 h-3 text-muted-foreground" />
              <input
                autoFocus
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search problems..."
                className="flex-1 bg-transparent text-[11px] outline-none placeholder:text-muted-foreground/50"
              />
            </div>
            <div className="flex-1 overflow-y-auto">
              {filtered.length === 0 && (
                <div className="px-3 py-4 text-center text-[11px] text-muted-foreground/50">
                  No problems found
                </div>
              )}
              {filtered.map((p) => (
                <button
                  key={p.problem_id}
                  onClick={() => {
                    onSelect?.(p.problem_id);
                    setOpen(false);
                    setQuery('');
                  }}
                  className={`w-full text-left px-3 py-2 hover:bg-muted/50 transition-colors ${selectedId === p.problem_id ? 'bg-primary/10' : ''}`}
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="text-[11px] font-medium text-foreground truncate">{p.title}</span>
                    {p.difficulty && (
                      <span className={`text-[9px] px-1.5 py-0.5 rounded font-medium shrink-0 ${DIFF_COLORS[p.difficulty] || ''}`}>
                        {p.difficulty}
                      </span>
                    )}
                  </div>
                  <div className="text-[9px] text-muted-foreground/60 mt-0.5">
                    {p.method_name}() · {p.pattern}
                  </div>
                </button>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default memo(ProblemSelector);
