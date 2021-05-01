import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
} from "react-router-dom";

import Page from "./Page";
import { generateVersePagePath } from "./utils";

import './App.css';

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/app/" render={() =>
          <Redirect to={generateVersePagePath(1, 1)} />
        }/>
        <Route path={generateVersePagePath(":suraNum", ":ayahNum")} children={<Page />} />
      </Switch>
    </Router>
  );
}

export default App;
