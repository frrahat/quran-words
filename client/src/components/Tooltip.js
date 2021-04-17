import React, { useState } from 'react';

import './Tooltip.css';

function Tooltip({text, childRef, children}) {
  const [isTooltipTextVisible, setTooltipTextVisible] = useState();
  const [tooltipPositionStyle, setTooltipPositionStyle] = useState();

  const onMouseEnterHandler = () => {
    const { top } = childRef.current.getBoundingClientRect();

    setTooltipPositionStyle({
      top: `${top - 32}px`,
    });

    setTooltipTextVisible(true);
  };

  const onMouseLeaveHandler = () => setTooltipTextVisible(false);

  return (
    <div onMouseEnter={onMouseEnterHandler} onMouseLeave={onMouseLeaveHandler}>
      { isTooltipTextVisible && <div className="Tooltip-text" style={tooltipPositionStyle}>{text}</div> }
      {children}
    </div>
  )
}

export default Tooltip;
