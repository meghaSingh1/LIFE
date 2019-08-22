import React, {Component} from 'react';
import axios from 'axios'
import {Link} from 'react-router-dom'
import { Button, Popup } from 'semantic-ui-react'
import logo from '../assets/images/logo.png'


export default class Navbar extends Component {
    constructor(props) {
      super(props);
    }

    handleLogout = () => {
        localStorage.clear();
        this.props.history.push('/login');
    }
  
    render() {
      return (
        <div style={{backgroundColor: 'white', padding: '5px 5px'}} class="ui secondary menu">
            <a href='/' style={{padding: '0px 5px'}} class="header item header-logo"><img style={{width: '130px'}} src={logo} alt="Logo" /></a>

                <a href='/' class="item">Home</a>
                <a class="item">Home</a>
                <a href='/following' class="item">Home</a>
            <div class="right menu">
            <div class="item">
                <div class="ui icon input">
                <input style={{width: '100%'}} type="text" placeholder="Search..." />
                <i aria-hidden="true" class="search icon"></i>
                </div>
            </div>
            <Popup on='click' style={{padding: '0px'}} position = 'bottom center'
            trigger={<button style={{padding: '0'}} class="ui button item"><i aria-hidden="true" class="bell outline icon large"></i><div class="floating ui red label">22</div></button>}>
                <div>
                    <div class="ui vertical menu">
                        <a href="//google.com" target="_blank" class="item">Visit Google</a>
                        <div class="link item">Link via prop</div>
                        <a class="item">Javascript Link</a>
                    </div>
                </div>
            </Popup>
            <Popup on='click' style={{padding: '0px'}} position = 'bottom right'
            trigger={<button class="ui button item"><img class="ui avatar image" src="http://127.0.0.1:8000/static/images/avatar/anon.jpg" /></button>}>
                <div>
                    <div class="ui vertical menu">
                        <a href={'/profile/' + localStorage.getItem('profile_name')} class='item'>Profile</a>
                        <Link class='item'>Setting</Link>
                        <Link class='item' onClick={this.handleLogout}>Logout</Link>
                    </div>
                </div>
            </Popup>
            </div>
        </div>
      );
    }
}