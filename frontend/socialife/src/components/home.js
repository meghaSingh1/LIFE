import React, {Component} from 'react';
import axios from 'axios'
import {Link} from 'react-router-dom'
import Navbar from './navbar'
import PostList from './postList'

export default class Login extends Component {
    constructor(props) {
      super(props);
      this.state = {
          email: '',
          text_content: null,
          user_posts: null,
      }
    }

    componentDidMount() {
        const email = localStorage.getItem('email');
        const token = localStorage.getItem('token');
        axios.post('http://127.0.0.1:8000/api/check_logged_in', {email: email}, {headers: 
        {'Content-Type': 'application/x-www-form-urlencoded',
         'Authorization': "Bearer " + token}})
         .then(res => {
            if (res.status != 200) {
                localStorage.clear();
                this.props.history.push('/login');
            }
        }).catch(err => {
            localStorage.clear();
            this.props.history.push('/login');
        })

        this.requestPosts();
    }

    requestPosts = () => {
        const email = localStorage.getItem('email');
        const token = localStorage.getItem('token');

        axios.post('http://127.0.0.1:8000/api/get_feed_posts', {email: email}, {headers: 
        {'Content-Type': 'application/x-www-form-urlencoded',
         'Authorization': "Bearer " + token}})
         .then(res => {
            if (res.status === 200)
                this.setState({user_posts: res.data.user_posts});
        }).catch(err => {})
    }
  
    render() {

        return (
            <div class='background'>
                <Navbar history={this.props.history} profile_name={this.state.use}/>
                <div class='container feed-container'>
                    <div class="ui items">
                        <PostList posts={this.state.user_posts} isHomePage={true} allowToPost={true} requestPosts={this.requestPosts} />
                    </div>
                </div>
            </div>
        );
    }
  }