import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
} from "react-router-dom";

import Page from "./Page";
import { getVersePageLink } from "./utils";

import './App.css';

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" render={() =>
          <Redirect to={getVersePageLink(1, 1)} />
        }/>
        <Route path={getVersePageLink(":suraNum", ":ayahNum")} children={<Page />} />
      </Switch>
    </Router>
  );
}

export default App;
