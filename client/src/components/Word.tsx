import { useRef, MouseEventHandler } from "react";
import Tooltip from "./Tooltip";

import './Word.scss';

function Word({
  arabic,
  translation,
  onClickHandler,
  isSelected,
  isHighlighted, }: {
    arabic: string,
    translation: string,
    onClickHandler: MouseEventHandler<HTMLDivElement>,
    isSelected: boolean,
    isHighlighted: boolean,
  }) {
  const wordRef = useRef(null);

  return (
    <Tooltip text={translation} childRef={wordRef}>
      <div
        className={`Word${isSelected ? ' Word-selected' : ''}${isHighlighted ? ' Word-highlighted' : ''}`}
        ref={wordRef} onClick={onClickHandler}
      >
        {arabic}
      </div>
    </Tooltip>
  )
}

export default Word;
