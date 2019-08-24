import React, {Component} from 'react';
import axios from 'axios'
import {Link} from 'react-router-dom'
import Navbar from './navbar'
import PostList from './postList'
import ImageUploader from 'react-images-upload'


export default class Login extends Component {
    constructor(props) {
      super(props);
      this.state = {
          email: '',
          text_content: null,
          user_posts: null,
          pictures: []
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

    onDrop = (pictureFiles) => {
        const email = localStorage.getItem('email');
        const token = localStorage.getItem('token');
        if(pictureFiles.length > 0) {
            console.log(pictureFiles[0]);

            let formData = new FormData(); 
            formData.append('file', pictureFiles[0]); 
            formData.append('email', email);
            for (var pair of formData.entries()) { console.log(pair[0]+ ', ' + pair[1]); }
            axios.post('http://127.0.0.1:8000/api/upload_picture', formData, {headers: 
            {'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': "Bearer " + token}}).then(res => {
            }).catch(err => console.log(err));
        }
    }

    clickWebSocket = () => {

        console.log(this.state.message);
        console.log('ha')
    }

    render() {
        return (
            <div class='background'>
                <Navbar history={this.props.history} profile_name={this.state.use}/>
                <div class='feed-container'>
                    <div class='ui grid'>
                    <div class='four wide column feed-column'>
                        <div class="ui vertical menu">
                        <ImageUploader class='item'
                            withIcon={true} singleImage={true} withLabel={true}
                            buttonText='Choose images'
                            onChange={this.onDrop}
                            imgExtension={['.jpg', '.gif', '.png', '.gif']}
                            maxFileSize={5242880} withPreview={true}
                        />
                        <button onClick={this.clickWebSocket} class='ui button'>Websocket</button>
                        <a class="item">
                        <i style={{float: 'right'}} aria-hidden="true" class="info icon large"></i>
                            About
                        </a>
                        <a class="item">
                            <i style={{float: 'right'}} aria-hidden="true" class="setting icon large"></i>
                            Setting
                        </a>
                        <div class="item">
                            <div class="ui icon input">
                            <input type="text" placeholder="Search mail..." />
                            <i aria-hidden="true" class="search icon"></i>
                            </div>
                        </div>
                    </div></div>
                    <div class='twelve wide column feed-column'>
                        <div>
                            <PostList posts={this.state.user_posts} isHomePage={true} allowToPost={true} requestPosts={this.requestPosts} />
                        </div>
                    </div>
                    </div>
                </div>
            </div>
        );
    }
  }