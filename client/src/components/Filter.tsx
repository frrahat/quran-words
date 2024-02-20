import { MouseEventHandler, ReactElement, useState } from "react";

import "./Filter.scss";

function Filter({
  filterLabel,
  filterValue,
  selectorComponent,
  onClearAction,
}: {
  filterLabel: string;
  filterValue: boolean | string | number | null | undefined;
  selectorComponent: ReactElement;
  onClearAction: () => void;
}) {
  const isUnset = filterValue === null || filterValue === undefined;
  const [shouldShowUnsetView, setShouldShowUnsetView] =
    useState<boolean>(isUnset);

  const handleClickOnUnsetView: MouseEventHandler<HTMLDivElement> = (event) => {
    event.stopPropagation();
    event.preventDefault();
    setShouldShowUnsetView(false);
  };

  const handleClickOnClear: MouseEventHandler<HTMLDivElement> = (event) => {
    event.stopPropagation();
    event.preventDefault();
    setShouldShowUnsetView(true);
    onClearAction();
  };

  return (
    <div className="Filter">
      <div className="Filter-Label">{filterLabel} : </div>
      <div className="Filter-Selector">
        {shouldShowUnsetView ? (
          <div
            className="Filter-Selector-unsetView"
            onClick={handleClickOnUnsetView}
          >
            Not Set
          </div>
        ) : (
          selectorComponent
        )}
      </div>
      {!isUnset && (
        <div className="Filter-ClearButton" onClick={handleClickOnClear}>
          Clear
        </div>
      )}
    </div>
  );
}

export default Filter;
