import { useHistory } from "react-router-dom";

import './Paginator.scss';

function PaginatorButton({ link, text, isDisabled, onPostPageNavigation }: {
  link: string,
  text: string,
  isDisabled: boolean,
  onPostPageNavigation?: Function,
}) {
  const history = useHistory();

  return (
    <button
      className="Paginator-btn"
      disabled={isDisabled}
      onClick={(event) => {

        history.push(link);

        event.preventDefault();
        event.stopPropagation();

        if (onPostPageNavigation) {
          onPostPageNavigation();
        }
      }}
    >
      {text}
    </button>
  )
}

function Paginator({ currentPage, max, getPageLink, onPostPageNavigation }: {
  currentPage: number,
  max: number,
  getPageLink: (pageNum: number) => string,
  onPostPageNavigation?: Function,
}) {
  return (
    <div className="Paginator">
      <PaginatorButton
        link={getPageLink(currentPage - 1)}
        text='Prev'
        isDisabled={currentPage <= 1}
        onPostPageNavigation={onPostPageNavigation}
      />
      <PaginatorButton
        link={getPageLink(currentPage + 1)}
        text='Next'
        isDisabled={currentPage >= max}
        onPostPageNavigation={onPostPageNavigation}
      />
    </div>
  )
}

export default Paginator;
