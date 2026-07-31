export function TrendChart({ data, height = 160 }) {
  if (!data || data.length === 0)
    return <div className="text-sm text-[#94A3B8] py-8 text-center">No trend data</div>;

  const max = Math.max(...data.map((d) => d.value), 1);
  const w = 600;
  const h = height;
  const pad = { top: 20, right: 16, bottom: 24, left: 40 };
  const cw = w - pad.left - pad.right;
  const ch = h - pad.top - pad.bottom;

  const points = data.map((d, i) => ({
    x: pad.left + (i / Math.max(data.length - 1, 1)) * cw,
    y: pad.top + ch - (d.value / max) * ch,
    ...d,
  }));

  const linePath = points.map((p, i) => `${i === 0 ? "M" : "L"}${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(" ");

  const areaPath =
    linePath +
    ` L${points[points.length - 1].x.toFixed(1)},${pad.top + ch} L${points[0].x.toFixed(1)},${pad.top + ch} Z`;

  const yTicks = [0, Math.round(max / 2), max];

  return (
    <svg viewBox={`0 0 ${w} ${h}`} className="w-full" style={{ height: h }}>
      {/* Grid lines */}
      {yTicks.map((t) => (
        <line
          key={t}
          x1={pad.left}
          y1={pad.top + ch - (t / max) * ch}
          x2={w - pad.right}
          y2={pad.top + ch - (t / max) * ch}
          stroke="#E2E8F0"
          strokeWidth="1"
        />
      ))}
      {/* Y labels */}
      {yTicks.map((t) => (
        <text
          key={t}
          x={pad.left - 8}
          y={pad.top + ch - (t / max) * ch + 4}
          textAnchor="end"
          className="text-[10px] fill-[#94A3B8]"
        >
          {t}
        </text>
      ))}

      {/* Area */}
      <path d={areaPath} fill="url(#grad)" opacity="0.4" />
      <defs>
        <linearGradient id="grad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#4F46E5" stopOpacity="0.3" />
          <stop offset="100%" stopColor="#4F46E5" stopOpacity="0" />
        </linearGradient>
      </defs>

      {/* Line */}
      <path d={linePath} fill="none" stroke="#4F46E5" strokeWidth="2" strokeLinejoin="round" strokeLinecap="round" />

      {/* Dots */}
      {points.map((p, i) => (
        <circle key={i} cx={p.x} cy={p.y} r="3" fill="#4F46E5" stroke="white" strokeWidth="1.5" />
      ))}

      {/* X labels */}
      {points.map((p, i) =>
        data.length > 12 ? i % Math.ceil(data.length / 8) === 0 : true ? (
          <text
            key={i}
            x={p.x}
            y={h - 4}
            textAnchor="middle"
            className="text-[10px] fill-[#94A3B8]"
          >
            {p.label}
          </text>
        ) : null
      )}
    </svg>
  );
}

export function MiniBar({ value, max, color = "#4F46E5", height = 6 }) {
  const p = max > 0 ? (value / max) * 100 : 0;
  return (
    <div className="bg-[#F1F5F9] rounded-full overflow-hidden" style={{ height }}>
      <div
        className="rounded-full transition-all"
        style={{ width: `${p}%`, height, backgroundColor: color }}
      />
    </div>
  );
}

export function BarRow({ label, value, max, color = "#4F46E5", right }) {
  return (
    <div className="grid grid-cols-[80px_1fr_50px] items-center gap-3 py-1.5">
      <span className="text-sm text-[#475569] truncate">{label}</span>
      <MiniBar value={value} max={max} color={color} />
      <span className="text-sm font-medium text-right text-[#0F172A] tabular-nums">
        {right || value}
      </span>
    </div>
  );
}
