/**
 * TestResultsPanel.jsx
 * LeetCode-style test results panel.
 * Shows pass/fail per test, input/expected/actual, console, exception.
 * Clicking a test triggers replay (visualization of that test).
 */
import { memo, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, XCircle, ChevronDown, Clock, Cpu, AlertTriangle } from 'lucide-react';

function formatValue(v) {
  if (v === null || v === undefined) return 'null';
  if (typeof v === 'object') return JSON.stringify(v);
  return String(v);
}

function formatTime(s) {
  if (s == null) return '—';
  if (s < 0.001) return '<1ms';
  if (s < 1) return `${Math.round(s * 1000)}ms`;
  return `${s.toFixed(3)}s`;
}

function TestResultsPanel({ testResults = [], statistics, onReplayTest, replayTestIdx }) {
  if (!testResults.length) {
    return (
      <div className="px-4 py-3 text-[11px] text-muted-foreground/50 italic">
        No test results. Run a solution to see results.
      </div>
    );
  }

  const passed = testResults.filter((t) => t.passed).length;
  const total = testResults.length;
  const passPct = total > 0 ? Math.round((passed / total) * 100) : 0;

  return (
    <div className="h-full flex flex-col overflow-hidden">
      {/* Header: pass/fail summary */}
      <div className="px-4 py-3 border-b border-border shrink-0">
        <div className="flex items-center justify-between mb-2">
          <span className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground/60">
            Test Results
          </span>
          <span className={`text-[10px] font-mono font-bold ${passed === total ? 'text-emerald-500' : 'text-destructive'}`}>
            {passed}/{total} Passed
          </span>
        </div>
        <div className="h-1.5 rounded-full bg-muted overflow-hidden">
          <motion.div
            className={`h-full ${passed === total ? 'bg-emerald-500' : 'bg-amber-500'}`}
            initial={{ width: 0 }}
            animate={{ width: `${passPct}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </div>

      {/* Test cards */}
      <div className="flex-1 overflow-y-auto px-2 py-2">
        {testResults.map((t) => (
          <TestCard
            key={t.testIdx}
            test={t}
            isReplay={replayTestIdx === t.testIdx}
            onReplay={() => onReplayTest?.(t.testIdx)}
          />
        ))}
      </div>

      {/* Footer: statistics */}
      {statistics && (
        <div className="px-4 py-2 border-t border-border shrink-0 grid grid-cols-3 gap-2 text-[10px]">
          <Stat label="Pass %" value={`${statistics.pass_percentage}%`} />
          <Stat label="Avg" value={formatTime(statistics.avg_runtime)} />
          <Stat label="Worst" value={formatTime(statistics.worst_runtime)} />
          <Stat label="Fastest" value={formatTime(statistics.fastest_runtime)} />
          <Stat label="Passed" value={statistics.passed_tests} />
          <Stat label="Failed" value={statistics.failed_tests} />
        </div>
      )}
    </div>
  );
}

function TestCard({ test, isReplay, onReplay }) {
  const [expanded, setExpanded] = useState(!test.passed);
  const hasDetail = !test.passed || test.exception || test.consoleOutput;

  return (
    <div className={`mb-1.5 rounded-md border ${test.passed ? 'border-emerald-500/20 bg-emerald-500/5' : 'border-destructive/30 bg-destructive/5'} ${isReplay ? 'ring-1 ring-primary' : ''}`}>
      <button
        className="w-full flex items-center gap-2 px-2.5 py-1.5 text-left"
        onClick={() => hasDetail && setExpanded((e) => !e)}
      >
        {test.passed ? (
          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
        ) : (
          <XCircle className="w-3.5 h-3.5 text-destructive shrink-0" />
        )}
        <span className="text-[11px] font-medium text-foreground truncate flex-1">
          {test.description || `Test ${test.testIdx + 1}`}
        </span>
        {test.executionTime != null && (
          <span className="text-[9px] text-muted-foreground/60 font-mono flex items-center gap-0.5">
            <Clock className="w-2.5 h-2.5" />
            {formatTime(test.executionTime)}
          </span>
        )}
        {hasDetail && (
          <ChevronDown className={`w-3 h-3 text-muted-foreground transition-transform ${expanded ? 'rotate-180' : ''}`} />
        )}
      </button>

      <AnimatePresence>
        {expanded && hasDetail && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="overflow-hidden"
          >
            <div className="px-2.5 pb-2 space-y-1.5">
              {test.inputRepr && (
                <DetailRow label="Input" value={test.inputRepr} />
              )}
              {!test.passed && test.expected != null && (
                <DetailRow label="Expected" value={formatValue(test.expected)} color="text-emerald-600 dark:text-emerald-400" />
              )}
              {!test.passed && test.actual != null && (
                <DetailRow label="Actual" value={formatValue(test.actual)} color="text-destructive" />
              )}
              {test.consoleOutput && (
                <DetailRow label="Console" value={test.consoleOutput} mono />
              )}
              {test.exception && (
                <div className="text-[10px] font-mono text-destructive bg-destructive/10 rounded px-2 py-1 break-all">
                  <AlertTriangle className="w-3 h-3 inline mr-1" />
                  {test.exception}
                </div>
              )}
              {!test.passed && (
                <button
                  onClick={onReplay}
                  className="text-[10px] text-primary hover:underline mt-1"
                >
                  ▶ Visualize this test
                </button>
              )}
              {test.passed && isReplay && (
                <span className="text-[10px] text-primary">▶ Currently visualized</span>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function DetailRow({ label, value, color = '', mono = false }) {
  return (
    <div className="flex gap-2 text-[10px]">
      <span className="text-muted-foreground/60 min-w-[50px]">{label}</span>
      <span className={`${mono ? 'font-mono' : 'font-mono'} ${color} text-foreground/80 break-all`}>
        {value}
      </span>
    </div>
  );
}

function Stat({ label, value }) {
  return (
    <div className="flex flex-col">
      <span className="text-[9px] text-muted-foreground/50 uppercase">{label}</span>
      <span className="text-[10px] font-mono font-semibold text-foreground/80">{value}</span>
    </div>
  );
}

export default memo(TestResultsPanel);
