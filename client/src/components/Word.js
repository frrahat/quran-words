import { useRef } from "react";
import Tooltip from "./Tooltip";

import './Word.css';

function Word({word_id, arabic, translation}) {
  const wordRef = useRef(null);

  return (
    <Tooltip text={translation} childRef={wordRef}>
      <div className="Word" ref={wordRef}>
        <div className="Word-arabic" id={`word-ar-${word_id}`}>
          {arabic}
        </div>
      </div>
    </Tooltip>
  )
}

export default Word;
