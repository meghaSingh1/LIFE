import React, {Component} from 'react';
import './App.css'
import {BrowserRouter as Router, Route, Link} from 'react-router-dom'
import Login from './components/login'
import Signup from './components/signup'
import Home from './components/home'
import UserProfile from './components/userProfile'

function App() {
  return (
    <Router>
      <div>
        <Route path="/login" exact component={Login} />
        <Route path="/signup" exact component={Signup} />
        <Route path="/" exact component={Home} />
        <Route path="/profile/:profileName" component={UserProfile} />
      </div>
    </Router>
  );
}

export default App;
