import React, {Component} from 'react';
import axios from 'axios'
import {Link} from 'react-router-dom'
import logo from '../assets/images/logo.png';

export default class Login extends Component {
    constructor(props) {
      super(props);
      this.state = {
        email: '',
        password: '',
        error: false,
      }
    }

    UNSAFE_componentWillMount() {
      const email = localStorage.getItem('email');
      const token = localStorage.getItem('token');
      axios.post('http://127.0.0.1:8000/api/check_logged_in', {email: email}, {headers: 
      {'Content-Type': 'application/x-www-form-urlencoded',
       'Authorization': "Bearer " + token}})
        .then(res => {
            if (res.status == 200)
                this.props.history.push('/');
            else               
                localStorage.clear();
        }).catch(err => {
            localStorage.clear();
        })
    }
  
    handleSubmit = (e) => {
      e.preventDefault();
      console.log(this.state.email);
      axios.post('http://127.0.0.1:8000/api/token/', {email: this.state.email, password: this.state.password}).then(res => {
        if (res.status == 200) {
          localStorage.setItem('token', res.data.access);
          localStorage.setItem('email', res.data.email);
          this.props.history.push('/')
        }
        else
          this.setState({error: true})
      }).catch(err => this.setState({error: true}))
    }
  
    render() {
      const errorMessage = this.state.error ? ( 
      <div class="ui error message">
        <div class="content">
          <h4 class="header">Log In failed</h4>
          <p style={{fontSize: '1rem'}}>No active account found with the given credentials</p>
        </div>
      </div>) : '';
      return (
        <div className="login-screen">
            <div class="ui text container login-wrapper">
                <div class="ui card login-card">
                    <div class="content login-form-header">
                        <img class='login-form-logo' src={logo} alt="Logo" />
                    </div>
                    <div class="content">
                    <form onSubmit={this.handleSubmit} class="ui form">
                        <div class="field required">
                        <label>Email Address</label>
                        <div class="ui input input-wrapper">
                            <div class='input-icon'><i aria-hidden="true" class="user icon"></i></div>
                            <input style={{border: 'None'}} placeholder="Email Address" value={this.state.email} onChange={e => this.setState({email: e.target.value})} />
                        </div>
                        </div>
                        <div class="field required">
                        <label>Password</label>
                        <div class="ui input input-wrapper">
                            <div class='input-icon'><i aria-hidden="true" class="lock icon"></i></div>
                            <input type='password' style={{border: 'None'}} placeholder="Password" value={this.state.password} onChange={e => this.setState({password: e.target.value})} />
                        </div>
                        </div>
                        <button type="submit" class="ui blue button login-form-buttons">Login</button>
                    </form>
                    {errorMessage}
                    <div style={{textAlign:'center'}}>
                        <div class="ui horizontal divider">Or</div>
                        <button onClick={() => this.props.history.push('/signup')} class="ui button login-form-buttons">
                            <i aria-hidden="true" class="signup icon"></i>Sign up
                        </button>
                    </div>
                    </div>
                </div>
            </div>
        </div>
      );
    }
  }