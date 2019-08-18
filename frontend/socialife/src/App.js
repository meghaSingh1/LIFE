import React, {Component} from 'react';
import './App.css'
import {BrowserRouter as Router, Route, Link} from 'react-router-dom'
import Login from './components/login'
import Home from './components/home'

function App() {
  return (
    <Router>
      <div>
        <Route path="/login" exact component={Login} />
        <Route path="/" exact component={Home} />
      </div>
    </Router>
  );
}

export default App;
