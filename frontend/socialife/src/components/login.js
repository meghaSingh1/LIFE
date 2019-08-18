import React, {Component} from 'react';
import axios from 'axios'
import {Link} from 'react-router-dom'


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
       .then(data => {
          if (data.status == 200)
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
        <div className="App">
          <div style={{width: '24em', paddingTop: '10em', textAlign: 'left'}} class="ui text container">
            <div style={{width: '24em'}} class="ui card">
            <div style={{backgroundColor: '#2185d0', padding: '0.6em 1em'}} class="content blue"><div style={{color: 'white', fontWeight: 'normal'}} class="header">Sign In</div></div>
            <div class="content">
            <form onSubmit={e => this.handleSubmit(e)} class="ui form">
              <div class="field required">
                <label>Email Address</label>
                <div style={{border: '1px solid #ccc'}} class="ui input">
                  <div style={{height: '100%', borderRight: '1px solid #ccc', padding: '.67857143em 1em'}}><i aria-hidden="true" style={{lineHeight: '1.21428571em', fontSize: '1em'}} class="user icon"></i></div>
                  <input style={{border: 'None'}} placeholder="Email Address" value={this.state.email} onChange={e => this.setState({email: e.target.value})} />
                </div>
              </div>
              <div class="field required">
                <label>Password</label>
                <div style={{border: '1px solid #ccc'}} class="ui input">
                  <div style={{height: '100%', borderRight: '1px solid #ccc', padding: '.67857143em 1em'}}><i aria-hidden="true" style={{lineHeight: '1.21428571em', fontSize: '1em'}} class="lock icon"></i></div>
                  <input type='password' style={{border: 'None'}} placeholder="Password" value={this.state.password} onChange={e => this.setState({password: e.target.value})} />
                </div>
              </div>
              <button style={{width: '100%', fontWeight: 'normal'}} type="submit" class="ui blue button">Login</button>
            </form>
            {errorMessage}
            </div>
            </div>
          </div>
        </div>
      );
    }
  }