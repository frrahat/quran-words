import { SegmentData } from "../types";
import "./Segments.scss";

const segmentColors = [
  {
    'name': 'oragane',
    'value': '#e37010',
  },
  {
    'name': 'yellow',
    'value': '#ffff00',
  },
  {
    'name': 'purple',
    'value': '#bd80ff',
  },
  {
    'name': 'rose',
    'value': '#fd5162',
  },
  {
    'name': 'seaGreen',
    'value': '#32bd2f',
  },
  {
    'name': 'sky',
    'value': '#548dd4',
  }
];


function Segments({ segments, translation }: {
  segments: SegmentData[],
  translation: string,
}) {
  return (
    <div className="Segments">
      <div className="Segments-header">
        Segments
      </div>
      <div className="Segments-container">
        <div className="Segments-arabic">
          {
            segments.map(
              (segment, index) =>
                <span
                  key={`segarabic-${index}`}
                  style={{ color: segmentColors[index]?.value }}
                >
                  {segment.arabic}
                </span>
            )
          }
        </div>
        <div className="Segments-pos">
          {
            segments.map(
              (segment, index) =>
                <span
                  key={`segpos-${index}`}
                  className="Segments-pos-single"
                  style={{ color: segmentColors[index]?.value }}
                >
                  {segment.pos_full}
                </span>
            )
          }
        </div>
        <div className="Segments-translation">
          {translation}
        </div>
      </div>
    </div>
  )
}

export default Segments;
