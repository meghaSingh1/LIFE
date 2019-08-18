import React, {Component} from 'react';
import axios from 'axios'
import {Link} from 'react-router-dom'
import Navbar from './navbar'


export default class Login extends Component {
    constructor(props) {
      super(props);
      this.state = {
          email: '16520511@gm.uit.edu.vn',
          text_content: null
      }
    }

    componentDidMount() {
        const email = localStorage.getItem('email');
        const token = localStorage.getItem('token');
        axios.post('http://127.0.0.1:8000/api/check_logged_in', {email: email}, {headers: 
        {'Content-Type': 'application/x-www-form-urlencoded',
         'Authorization': "Bearer " + token}})
         .then(data => {
            if (data.status != 200) {
                localStorage.clear();
                this.props.history.push('/login');
            }
        }).catch(err => {
            localStorage.clear();
            this.props.history.push('/login');
        })
    }

    handleCreatePost = (e) => {
        e.preventDefault();
        const email = localStorage.getItem('email');
        const token = localStorage.getItem('token');
        axios.post('http://127.0.0.1:8000/api/create_new_post', {email: email, text_content: this.state.text_content}, {headers: 
        {'Content-Type': 'application/x-www-form-urlencoded',
         'Authorization': "Bearer " + token}})
         .then(data => {
             console.log(data);
            if (data.status == 201) 
                console.log('post created');
            else console.log('failed');
        }).catch(err => {
            console.log('failed');
        })
    }
  
    render() {
      return (
        <div>
            <Navbar history={this.props.history}/>
            <div class='container' style={{padding: '2em 15em'}}>
                <div class="ui pointing menu">
                    <a class="active item">What's on your mind right now?</a>
                </div>
                <div class="ui segment active tab">
                    <form class="ui form" onSubmit={this.handleCreatePost} method="post">
                        <div class='field'>
                            <textarea required onChange={e => this.setState({text_content: e.target.value})} style={{resize: 'none'}} placeholder="Tell us more" rows="3"></textarea>
                        </div>
                        <input type='submit' class="button ui" value="Post" />
                    </form>
                </div>
            </div>

        </div>
      );
    }
  }