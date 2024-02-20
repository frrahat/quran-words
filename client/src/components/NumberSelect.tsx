import { useState } from "react";

import "./NumberSelect.scss";

function NumberSelect({
  valueClassName,
  startNumber,
  endNumber,
  selectedNumber,
  onSelectNumber,
}: {
  valueClassName: string;
  startNumber: number;
  endNumber: number;
  selectedNumber: number;
  onSelectNumber: (num: number) => void;
}) {
  const [isOptionsExpanded, setIsOptionsExpanded] = useState(false);

  const totalNumbers = endNumber - startNumber + 1;
  return (
    <div
      className="NumberSelect"
      onClick={() => setIsOptionsExpanded(!isOptionsExpanded)}
    >
      <div className={valueClassName}>{selectedNumber}</div>
      <div
        className={`NumberSelect-Options${isOptionsExpanded ? "" : "-hidden"}`}
      >
        {
          // event propagation has been allowed intentionally to hide the dropdown on select
          Array(totalNumbers)
            .fill(null)
            .map((_1, index) => startNumber + index)
            .map((num) => (
              <div
                key={num}
                className="NumberSelect-Option"
                onClick={() => onSelectNumber(num)}
              >
                <span className="NumberSelect-Option-Num">{num}</span>
              </div>
            ))
        }
      </div>
    </div>
  );
}

export default NumberSelect;
