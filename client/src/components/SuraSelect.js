import { useState } from 'react';
import { suraList } from '../config';

import './SuraSelect.css'


function SuraSelect({ valueClassName, selectedSuraNum, onSelectSura }) {
  const [isOptionsExpanded, setIsOptionsExpanded] = useState(false);

  return (
    <div className="SuraSelect" onClick={() => setIsOptionsExpanded(!isOptionsExpanded)}>
      <div className={valueClassName}>
        { selectedSuraNum }
      </div>
      <div className={`SuraSelect-Options${isOptionsExpanded ? '': '-hidden'}`}>
        {
          // event propagation has been allowed intentionally to hide the dropdown on select
          suraList.map(({ id, name, meaning }) =>
          <div key={id} className="SuraSelect-Option" onClick={() => onSelectSura(id)}>
            <span className="SuraSelect-Option-Num">{id}</span>
            <span className="SuraSelect-Option-Name">{name}</span>
            <span className="SuraSelect-Option-Meaning">{meaning}</span>
          </div>
          )
        }
      </div>
    </div>
  )
}

export default SuraSelect;
