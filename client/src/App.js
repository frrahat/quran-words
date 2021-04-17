import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
} from "react-router-dom";

import Page from "./Page";

import './App.css';

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" render={() =>
          <Redirect to="/verses/1/1" />
        }/>
        <Route path="/verses/:suraNum/:ayahNum" children={<Page />} />
      </Switch>
    </Router>
  );
}

export default App;
