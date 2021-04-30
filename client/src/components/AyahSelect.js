import { useState } from "react";
import { suraList } from "../config";

import './AyahSelect.css';

function AyahSelect({ valueClassName, selectedSuraNum, selectedAyahNum, onSelectAyah }) {
  const [isOptionsExpanded, setIsOptionsExpanded] = useState(false);

  return (
    <div className="AyahSelect" onClick={() => setIsOptionsExpanded(!isOptionsExpanded)}>
      <div className={valueClassName}>
        { selectedAyahNum }
      </div>
      <div className={`AyahSelect-Options${isOptionsExpanded ? '': '-hidden'}`}>
        {
          // event propagation has been allowed intentionally to hide the dropdown on select
          Array.from(Array(suraList[selectedSuraNum - 1]?.ayah_count || 0).keys()).map( index =>
          <div key={index} className="AyahSelect-Option" onClick={() => onSelectAyah(index + 1)}>
            <span className="AyahSelect-Option-Num">{index + 1}</span>
          </div>
          )
        }
      </div>
    </div>
  )
}

export default AyahSelect;
