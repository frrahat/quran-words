import { Link } from "react-router-dom";

import './Paginator.scss';

function PaginatorButton({ link, text, isDisabled }: {
  link: string,
  text: string,
  isDisabled: boolean,
}) {
  return (
    <button
      className="Paginator-btn"
      disabled={isDisabled}
    >
      {
        isDisabled ? text : <Link to={link}>{text}</Link>
      }
    </button>
  )
}

function Paginator({ currentPage, max, getPageLink }: {
  currentPage: number,
  max: number,
  getPageLink: (pageNum: number) => string,
}) {
  return (
    <div className="Paginator">
      <PaginatorButton
        link={getPageLink(currentPage - 1)}
        text='Prev'
        isDisabled={currentPage <= 1}
      />
      <PaginatorButton
        link={getPageLink(currentPage + 1)}
        text='Next'
        isDisabled={currentPage >= max}
      />
    </div>
  )
}

export default Paginator;
