import { useRef } from "react";
import Tooltip from "./Tooltip";

import './Word.css';

function Word({arabic, translation, onClickHandler}) {
  const wordRef = useRef(null);

  return (
    <Tooltip text={translation} childRef={wordRef}>
      <div className="Word" ref={wordRef} onClick={onClickHandler}>
        {arabic}
      </div>
    </Tooltip>
  )
}

export default Word;
