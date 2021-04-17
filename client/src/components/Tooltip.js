import React, { useState } from 'react';

import './Tooltip.css';

function Tooltip({text, children}) {
  const [isTooltipTextVisible, setTooltipTextVisible] = useState();

  const onMouseEnterHandler = () => setTooltipTextVisible(true);
  const onMouseLeaveHandler = () => setTooltipTextVisible(false);

  return (
    <div onMouseEnter={onMouseEnterHandler} onMouseLeave={onMouseLeaveHandler}>
      { isTooltipTextVisible && <div className="Tooltip-text">{text}</div> }
      {children}
    </div>
  )
}

export default Tooltip;
