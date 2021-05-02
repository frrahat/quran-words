import { useRef, MouseEventHandler } from "react";
import Tooltip from "./Tooltip";

import './Word.css';

function Word({ arabic, translation, onClickHandler, isSelected }: {
  arabic: string,
  translation: string,
  onClickHandler: MouseEventHandler<HTMLDivElement>,
  isSelected: boolean,
}) {
  const wordRef = useRef(null);

  return (
    <Tooltip text={translation} childRef={wordRef}>
      <div className={`Word${isSelected ? '-selected' : ''}`} ref={wordRef} onClick={onClickHandler}>
        {arabic}
      </div>
    </Tooltip>
  )
}

export default Word;
