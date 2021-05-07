import { MouseEventHandler, useRef } from 'react';
import Tooltip from './Tooltip';
import Segments from './Segments';
import VerbForms from './VerbForms';
import { CorpusWordData } from '../types';

import './WordParts.scss';

function WordParts({ wordData, isWordRootPressed, onWordRootClickHandler }: {
  wordData: CorpusWordData,
  isWordRootPressed: boolean,
  onWordRootClickHandler: MouseEventHandler<HTMLDivElement>,
}) {
  const wordRootRef = useRef(null);

  const { english, segments, root, verb_forms } = wordData;

  return (
    <div className="WordParts">
      <div className="WordParts-item WordParts-segments">
        <Segments segments={segments} translation={english} />
      </div>
      {
        root &&
        <div className="WordParts-item WordParts-root">
          <div className="WordParts-root-header">
            Word Root
          </div>
          <div className="WordParts-root-container">
            <Tooltip
              text={`${isWordRootPressed ? 'Hide' : 'Show'} occurrences of this word root`}
              childRef={wordRootRef}
            >
              <div
                className={
                  `WordParts-root-content${isWordRootPressed ? ' WordParts-root-content-pressed' : ''
                  }`
                }
                onClick={onWordRootClickHandler}
                ref={wordRootRef}
              >
                {root}
              </div>
            </Tooltip>
          </div>
        </div>
      }
      {
        verb_forms &&
        <div className="WordParts-item WordParts-VerbForms">
          <VerbForms verbForms={verb_forms} />
        </div>
      }
    </div >
  )
}

export default WordParts;
