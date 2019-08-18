import React, {Component} from 'react';
import axios from 'axios'
import {Link} from 'react-router-dom'
import Navbar from './navbar'


export default class Login extends Component {
    constructor(props) {
      super(props);
      this.state = {
          email: '16520511@gm.uit.edu.vn',
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

        axios.post('http://127.0.0.1:8000/api/get_user_posts', {email: email}, {headers: 
        {'Content-Type': 'application/x-www-form-urlencoded',
         'Authorization': "Bearer " + token}})
         .then(res => {
            if (res.status === 200) {
                this.setState({user_posts: res.data.user_posts});
            }
        }).catch(err => {})
    }

    handleCreatePost = (e) => {
        e.preventDefault();
        const email = localStorage.getItem('email');
        const token = localStorage.getItem('token');
        axios.post('http://127.0.0.1:8000/api/create_new_post', {email: email, text_content: this.state.text_content}, {headers: 
        {'Content-Type': 'application/x-www-form-urlencoded',
         'Authorization': "Bearer " + token}})
        .then(data => {
            this.setState({text_content: ''})
            if (data.status == 201) 
                this.requestPosts();
            else console.log('failed');
        }).catch(err => {
            console.log('failed');
        })
    }
  
    render() {
        const post_items = this.state.user_posts === null ? 
        (<div class="ui active centered inline loader"></div>) : 
        this.state.user_posts.map(post => (         
            <div style={{border: '1px solid #ccc', padding: '12px 10px', backgroundColor: 'white'}} class="item">
                <div class="ui tiny image">
                <img src="http://127.0.0.1:8000/static/images/avatar/anon.jpg" />
                </div>
                <div class="content">
                <a class="header">{post.user.first_name + ' ' + post.user.last_name}</a>
                <div class="meta">{post.date_created}</div>
                <div class="description">
                    <p>{post.text_content}</p>
                </div>
                <div class="extra">
                    <i aria-hidden="true" class="red like icon large"></i>
                </div>
                </div>
            </div>
        ));

        return (
            <div style={{backgroundColor: '#f0eded'}}>
                <Navbar history={this.props.history}/>
                <div class='container' style={{padding: '2em 15%'}}>
                    <div class="ui pointing menu">
                        <a class="active item">What's on your mind right now?</a>
                    </div>
                    <div class="ui segment active tab">
                        <form class="ui form" onSubmit={this.handleCreatePost} method="post">
                            <div class='field'>
                                <textarea value={this.state.text_content} required onChange={e => this.setState({text_content: e.target.value})} style={{resize: 'none'}} placeholder="Tell us more" rows="3"></textarea>
                            </div>
                            <input type='submit' class="button ui blue" value="Post" />
                        </form>
                    </div>
                    <div class="ui items">
                        {post_items}
                    </div>
                </div>
            </div>
        );
    }
  }