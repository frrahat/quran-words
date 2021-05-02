import { useState } from 'react';

import './Tooltip.scss';

function Tooltip({ text, childRef, children }: {
  text: string,
  childRef: any,
  children: any,
}) {
  const [isTooltipTextVisible, setTooltipTextVisible] = useState(false);
  const [tooltipPositionStyle, setTooltipPositionStyle] = useState({
    bottom: 'unset'
  });

  const onMouseEnterHandler = () => {
    const { height } = childRef.current.getBoundingClientRect();
    setTooltipPositionStyle({
      bottom: `${height + 5}px`,
    });

    setTooltipTextVisible(true);
  };

  const onMouseLeaveHandler = () => setTooltipTextVisible(false);

  return (
    <div className="Tooltip" onMouseEnter={onMouseEnterHandler} onMouseLeave={onMouseLeaveHandler}>
      {
        isTooltipTextVisible &&
        <div className="Tooltip-text" style={tooltipPositionStyle}>
          {text}
        </div>
      }
      {children}
    </div>
  )
}

export default Tooltip;
