import React, { Component } from 'react';
import { Col, Row, Form, Button } from 'react-bootstrap';
import ReactModal from 'react-modal';
import { updateUserInfo, updateUserProfile } from '../../api/BLApi';
import '../../../../static/css/style2-light.css';
import { keyBy } from 'lodash';
import "./profile.css";

class EditProfileModal extends Component {
    constructor(props) {
        super(props);
        this.state = {
            errorMessage: "",
            recentInput: ["email", "phone_number", "birthday"],
            prevPhone: ""
        }
    }

    handleSubmit = (e) => {
        e.preventDefault();
        let reg = {
            email: /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/,
            phone_number: /^\(?([0-9]{3})\)?[-]?([0-9]{3})[-]?([0-9]{4})$/,
            birthday: /^(0?[1-9]|1[012])[\/\-](0?[1-9]|[12][0-9]|3[01])[\/\-]\d{4}$/
        }
        let errorMessages = {
            email: "Please provide a valid email address",
            phone_number: "Please provide a valid phone number",
            birthday: "Please provide birthday in the format of \"MM/DD/YYYY\""
        }

        var bad = false;

        for(let item of this.state.recentInput) {
            if (this.state[item] != null && !this.state[item].match(reg[item]) && this.state[item] !== "") {
                this.setState({errorMessage: errorMessages[item]});
                bad = true;
                break
            }
        }

        if (!bad) {
            let saveData = {...this.state}
            let keys = Object.keys(saveData)

            keys.forEach(key => {
                if(saveData[key].length === 0) {
                    delete saveData[key]
                }
            })

            this.setState({errorMessage:''})

            let formattedDate = saveData['birthday']
            
            if(saveData['birthday']) {
                let date = new Date(saveData['birthday'])
                formattedDate = `${date.getFullYear()}-${date.getMonth()+1}-${date.getDate()}`
                saveData = {...saveData, birthday: formattedDate}
            }

            if(saveData['email'] === "") {
                delete saveData['email']
            }

            if(saveData['phone_number'] === "") {
                delete saveData['phone_number']
            }

            updateUserInfo( saveData , this.props.userId).then(data => {
                this.props.updateStateFunc()
                this.props.close()
            })
            updateUserProfile( saveData , this.props.profileId).then(data => {
                this.props.updateStateFunc()
                this.props.close()
            })
            this.setState({errorMessage: ""});
        }
    }

    handleClose = () => {
        this.setState({errorMessage:"", birthday:"", phone_number:"", email:""});
        this.props.close()
    }

    handleChange = (field) => {
        if(this.state.recentInput[0] !== field) {
            if(this.state.recentInput[1] === field) {
                let input = [...this.state.recentInput]
                input[1] = input[0]
                input[0] = field
                this.setState({recentInput: input})
            }
            if(this.state.recentInput[2] === field) {
                let input = [...this.state.recentInput]
                input[2] = input[1]
                input[1] = input[0]
                input[0] = field
                this.setState({recentInput: input})
            }
        }
    }

    formatPhone = (input) => {
        if(input.length > this.state.prevPhone.length) {
            if(input.length > 14) {
                input = input.slice(0,14)
            } else if(input.length === 10) {
                input = input.slice(0,9) + '-' + input.slice(9)
            } else if(input.length === 4) {
                if (input.slice(0,1) === '(') {
                    input = input + ') '
                } else
                    input = '(' + input.slice(0,3) + ') ' + input.slice(3)
            }

        }   else if (input.length < this.state.prevPhone.length) {
                let lastChar = input.slice(input.length-1)
                if(lastChar === '-') {
                    input = input.slice(0, input.length-1)
                } else if(lastChar === ' ') {
                    input = input.slice(1, 4)
                } 
                else if (input === '(') {
                    input = ''
                }
        }

        return input
    }

    render() {  
        const userItems = this.props.edit.user.map(item => 
            <Form.Group as={Row}>
            
            <Form.Label column md={4}>
                {item.name}
            </Form.Label>
            
            <Col ReactModal={6}>
            <Form.Control type="text" placeholder={item.data} onChange={e => {
                this.setState({ [item.field]: e.target.value })
                if(item.field==='email') this.handleChange(item.field)
            }}/>
            </Col>
            </Form.Group>);

        const profileItems = this.props.edit.profile.map(item => {
            return item.name == 'Business Details' ?
                <Form.Group as={Row}>
                
                <Form.Label column md={4}>
                    {item.name}
                </Form.Label>
                
                <Col ReactModal={6}>
                <Form.Control as="textarea" rows={3} placeholder={item.data} onChange={e => this.setState({ [item.field]: e.target.value })}/>
                </Col>
                </Form.Group>
            :
                <Form.Group as={Row}>
                
                <Form.Label column md={4}>
                    {item.name}
                </Form.Label>
                
                <Col ReactModal={6}>
                    <Form.Control type="text" placeholder={item.data} onChange={e => {
                        this.formatPhone(e.target.value)
                        if(item.field === 'phone_number') {
                            let input = this.formatPhone(e.target.value)

                            this.setState({prevPhone: input})

                            e.target.value = input
                            if(input.includes('(')) input = input.replace('(', '')
                            if(input.includes(') ')) input = input.replace(') ', '')
                            if(input.includes('-')) input = input.replace('-', '')
                            this.setState({ [item.field]: input})
                        } else {
                            this.setState({ [item.field]: e.target.value })
                        }

                    if(item.field==='phone_number' || item.field==='birthday') this.handleChange(item.field)
                }}/>
                </Col>
                </Form.Group>
            });

        return (
            <ReactModal ariaHideApp={false} onRequestClose={this.handleClose} isOpen={this.props.isOpen} shouldCloseOnEsc={true} shouldCloseOnOverlayClick={true} className="modal-outer">
                <div className={`${this.props.edit.name === "Company Information" && "modal-inner-long"} user-profile`}>
                    <h2>Edit {this.props.edit.name}</h2>
                    <div className="profile-form-divider"></div>
                    <Form onSubmit={this.handleSubmit}>
                        {userItems}
                        {profileItems}
                        {this.state.errorMessage.length > 0 && <p style={{color: 'red'}}>{this.state.errorMessage}</p>}
                        <div className="d-flex flex-row justify-content-center">
                            <Button className="btn_profile_form_clear btn_clear" onClick={this.handleClose}>Close</Button>
                            <Button className="btn_profile_form btn_orange" type="submit">Submit</Button>
                        </div>
                    </Form>
                </div>
            </ReactModal>
        )
    }
}

export default EditProfileModal;