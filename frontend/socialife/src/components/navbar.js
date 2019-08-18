import React, {Component} from 'react';
import axios from 'axios'
import {Link} from 'react-router-dom'


export default class Navbar extends Component {
    constructor(props) {
      super(props);
    }

    handleLogout = () => {
        localStorage.clear();
        this.props.history.push('login');
    }
  
    render() {
      return (
        <div class="ui secondary menu">
            <Link to='/' class="active item">Home</Link>
            <Link to='/profile' class="item">Home</Link>
            <Link to='/following' class="item">Home</Link>
            <div class="right menu">
            <div class="item">
                <div class="ui icon input">
                <input type="text" placeholder="Search..." />
                <i aria-hidden="true" class="search icon"></i>
                </div>
            </div>
            <Link onClick={this.handleLogout} class="item">Logout</Link>
            </div>
        </div>
      );
    }
}