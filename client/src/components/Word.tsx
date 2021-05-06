import { MouseEventHandler } from "react";

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
  return (
    <div
      className={`Word${isSelected ? ' Word-selected' : ''}${isHighlighted ? ' Word-highlighted' : ''}`}
      onClick={onClickHandler}
    >
      <div className="Word-arabic">
        {arabic}
      </div>
      <div className="Word-translation">
        {translation}
      </div>
    </div>
  )
}

export default Word;
