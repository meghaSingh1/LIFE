import React, {Component} from 'react';
import axios from 'axios'
import {Link} from 'react-router-dom'
import logo from '../assets/images/logo.png'
import { Popup } from 'semantic-ui-react'
import ReactDOM from 'react-dom'


export default class Navbar extends Component {
    constructor(props) {
        super(props);
        this.state = {
            requestUserIsAnonymous: null,
            notifications: null,
            newNotifications: 0,
        }
    }

    componentDidMount() {
        const email = localStorage.getItem('email');
        const token = localStorage.getItem('token');

        axios.post('http://127.0.0.1:8000/api/check_logged_in', {email: email}, {headers: 
        {'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': "Bearer " + token}})
        .then(res => {
            if (res.status == 200) {
                let newNotifications = 0;
                res.data.notifications.map(notification => {
                    if(!notification.is_read)
                        newNotifications += 1;
                })
                this.setState({requestUserIsAnonymous: false, notifications: res.data.notifications.slice(0, 7), newNotifications: newNotifications})
            }
            else this.setState({requestUserIsAnonymous: true});
        }).catch(err => {
            this.setState({requestUserIsAnonymous: true});
        })
    }

    handleLogout = () => {
        localStorage.clear();
        this.props.history.push('/login');
    }

    readNotifications = () => {
        this.setState({newNotifications: 0})
        
        const email = localStorage.getItem('email');
        const token = localStorage.getItem('token');

        axios.post('http://127.0.0.1:8000/api/read_notifications', {email: email}, {headers: 
        {'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': "Bearer " + token}})
        .then(res => {}).catch(err => {})
    }
  
    render() {
        const notifications = this.state.notifications != null ? 
        this.state.notifications.map(notification => (
            <Link to={notification.url} role="listitem" class="item list-item">
            <img src="https://react.semantic-ui.com/images/avatar/small/rachel.png" class="ui avatar image"/>
            <div class="content">
              <a class="header">{notification.from_user.first_name + ' ' + notification.from_user.last_name}</a>
              <div class="description">
                {notification.content}
              </div>
            </div>
          </Link>
        )) : '';

        return (
            this.state.requestUserIsAnonymous == null ?
            <div style={{backgroundColor: 'white', padding: '5px 5px'}} class="ui secondary menu">
            <a href='/' style={{padding: '0px 5px'}} class="header item header-logo"><img style={{width: '140px'}} src={logo} alt="Logo" /></a>
            </div> :
            this.state.requestUserIsAnonymous == true ?
            <div style={{backgroundColor: 'white', padding: '5px 5px'}} class="ui secondary menu">
            <a href='/' style={{padding: '0px 5px'}} class="header item header-logo"><img style={{width: '140px'}} src={logo} alt="Logo" /></a>
            </div> :
            <div>
            <div style={{backgroundColor: 'white', padding: '5px 5px'}} class="ui secondary menu">
                <a href='/' style={{padding: '0px 5px'}} class="header item header-logo"><img style={{width: '140px'}} src={logo} alt="Logo" /></a>
                <div class="right menu">
                <div class="item">
                    <div class="ui icon input">
                    <input style={{width: '100%'}} type="text" placeholder="Search..." />
                    <i aria-hidden="true" class="search icon"></i>
                    </div>
                </div>
                <button style={{padding: '.1em'}} class="ui button item"><i aria-hidden="true" class="mail outline icon large"></i><div class="floating ui red label">22</div></button>
                <Popup on='click' style={{padding: '0px'}} position = 'bottom center'
                trigger={<button onClick={this.readNotifications} style={{padding: '.1em'}} class="ui button item"><i aria-hidden="true" class="bell outline icon large"></i>{this.state.newNotifications == 0 ? '' : <div class="floating ui red label">{this.state.newNotifications}</div>}</button>}>
                    <div>
                        <div role="list" class="ui list notification-list">
                            <div style={{fontSize: '1.1em', fontWeight: '600'}} class='item notification-placeholder'>What's new?</div>
                            {notifications}
                            <div class='item notification-placeholder'><a>See more</a></div>
                        </div>
                    </div>
                </Popup>
                <Popup on='click' style={{padding: '0px'}} position = 'bottom right'
                trigger={<button class="ui button item"><img class="ui navbar-avatar image" src="http://127.0.0.1:8000/static/images/avatar/avatar.png" /></button>}>
                    <div>
                        <div class="navbar-user-menu ui vertical menu">
                            <div class='item navbar-user-menu-placeholder'>Welcome, {localStorage.getItem('profile_name')}!</div>
                            <a href={'/profile/' + localStorage.getItem('profile_name')} class='item'>
                                <i aria-hidden="true" class="address book outline icon"></i>Profile</a>
                            <Link class='item' onClick={this.handleLogout}>
                            <i aria-hidden="true" class="sign-out icon"></i>Logout</Link>
                        </div>
                    </div>
                </Popup>
                </div>
                </div>
            </div>
        );
    }
}