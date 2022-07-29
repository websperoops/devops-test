import React, { Component } from 'react'
import { getUserProfile, getUserInfo } from '../../api/BLApi';
import EditProfileModal from './EditProfileModal';
import ReferralsModal from './ReferralsModal/ReferralsModal'
import '../../../../static/css/style2-light.css';
import "./profile.css";

class MyProfile extends Component {

    constructor(props) {
        super(props);
        this.state = {
            profile: {},
            user: {},
            affiliate: "",
            showModal: false,
            edit: {
                name: null,
                user: [],
                profile: []
            },
            showReferralsModal: false,
        }
        this.closeModal = this.closeModal.bind(this)
        this.updateState = this.updateState.bind(this)
    }

    componentDidMount() {
        this.updateState()
    }

    closeModal() {
        this.setState({
            showModal: false
        })
    }

    updateState() {
        Promise.all([getUserProfile(), getUserInfo()])
            .then(data => { 
                this.setState(
                    {
                        profile: data[0].results[0],
                        user: data[1].results[0],
                        affiliate: data[0].results[0].affiliate_code

                    }
                )
            });
    }

    handleShowModal(name, user, profile) {
        this.setState({
            showModal: true,
            edit: {
                name,
                user,
                profile
            }
        })
    }

    formatPhoneNumber = (phone) => {
        if(phone) {
            return '(' + phone.slice(0,3) + ') ' + phone.slice(3,6) + '-' + phone.slice(6)
        }
    }

    handleShareClick = () => {
        navigator.clipboard.writeText(this.state.affiliate)
        this.handleShowReferralsModal()
    }

    handleShowReferralsModal = () => {
        this.setState({showReferralsModal: true})
    }

    handleCloseReferralsModal = () => {
        this.setState({showReferralsModal: false})
    }

    render() {
        const { user, profile, affiliate, showReferralsModal } = this.state
     
        const formatDate = (date) => {
            var parts = date.match(/(\d+)/g);
            let d = new Date(parts[0], parts[1]-1, parts[2])
            return `${d.getMonth() + 1}/${d.getDate()}/${d.getFullYear()}`;
        }
        return (
            <>
                {Object.entries(this.state.profile).length > 0 && <EditProfileModal
                    edit={this.state.edit}
                    isOpen={this.state.showModal}
                    close={this.closeModal}
                    userId={this.state.profile.user}
                    profileId={this.state.profile.id}
                    updateStateFunc={this.updateState}
                />}
                {
                    this.state.showReferralsModal && <ReferralsModal handleClose={this.handleCloseReferralsModal} affiliate_code={affiliate} showReferralsModal={showReferralsModal} username={this.state.user.first_name}/>
                }
                <div className="my-profile profile-section" id="my-profile">
                    <div className="">
                        <p className="profile-section-header">My Profile</p>
                    </div>
                    <div className="profile-section-subtitle">
                        <p>Basic Information</p>
                            <i onClick={() => {
                                this.handleShowModal('Basic Information',
                                [
                                    {
                                    name: 'First Name',
                                    field: 'first_name',
                                    data: user.first_name
                                    },
                                    {
                                    name: 'Last Name',
                                    field: 'last_name',
                                    data: user.last_name
                                    },
                                    {
                                    name: 'Email',
                                    field: 'email',
                                    data: user.email
                                    }
                                ],
                                [
                                    {
                                    name: 'Phone',
                                    field: 'phone_number',
                                    data: this.formatPhoneNumber(profile.phone_number)
                                    },
                                    {
                                    name: 'Location',
                                    field: 'location',
                                    data: profile.location
                                    }, 
                                    {
                                    name: 'Job Title',
                                    field: 'job_title',
                                    data: profile.job_title
                                    }, 
                                    {
                                    name: 'Birthday',
                                    field: 'birthday',
                                    data: formatDate(profile.birthday),
                                    }
                                ]
                                )}} className="fa fa-pencil">
                            </i>
                        
                    </div>
                    <div className="profile-section-info" style={{paddingRight: "0"}}>
                        <div className="profile-section-general-info">
                            <div className="profile-section-picture">
                                <img className="profile-section-img"
                                    src="data:image/png;base64,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"
                                    alt="profile-pic" />
                            </div>


                            <ul className="profile-section-general-info-list">
                                <li className="name-item">First Name: <span>{user.first_name}</span></li>
                                <li className="name-item">Last Name: <span>{user.last_name}</span></li>
                                <li>Member Since: <span>{user.date_joined && formatDate(user.date_joined)}</span></li>
                            </ul>
                        </div>

                        <ul className="profile-section-info-list">
                            <li>Phone Number: <span> {this.formatPhoneNumber(profile.phone_number)}</span></li>
                            <li>Email: <span> {user.email}</span></li>
                            <li>Location: <span>{profile.location}</span></li>
                            <li>Job Title: <span>{profile.job_title}</span></li>
                            <li>Birthday: <span>{profile.birthday && formatDate(profile.birthday)}</span></li>
                        </ul>

                    </div>
                    <div className="profile-section-subtitle">
                        <p>Company Information</p>
                        <i onClick={() => {
                                this.handleShowModal('Company Information',
                                [],
                                [
                                    {
                                    name: 'Business Name',
                                    field: 'business_name',
                                    data: profile.business_name
                                    },
                                    {
                                    name: 'Business Website',
                                    field: 'business_website',
                                    data: profile.business_website
                                    },
                                    {
                                    name: 'Industry Type',
                                    field: 'industry_type',
                                    data: profile.industry_type
                                    },
                                    {
                                    name: 'Industry Product',
                                    field: 'product_type',
                                    data: profile.product_type
                                    },
                                    {
                                    name: 'Number of Employees',
                                    field: 'employee_count',
                                    data: profile.employee_count
                                    }, 
                                    {
                                    name: 'Business Details',
                                    field: 'business_details',
                                    data: profile.business_details
                                    }, 
                                ]
                                )}} className="fa fa-pencil">
                            </i>
                    </div>
                    <div className="profile-section-info" style={{paddingRight: "0"}}>
                        <div className="profile-section-general-info">

                            <div className="profile-section-picture">
                                <img className="profile-section-img" style={{ borderRadius: '0%', filter: 'brightness(0%)' }}
                                    src="data:image/png;base64,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"
                                    alt="company-pic" />
                            </div>
                            <ul className="profile-section-general-info-list">
                                <li className="name-item">Business Name: <span>{profile.business_name}</span></li>
                            </ul>
                        </div>
                        <ul className="profile-section-info-list">
                            <li>Business Website: <span>{profile.business_website}</span></li>
                            <li>Industry Type: <span>{profile.industry_type}</span></li>
                            <li>Industry Product: <span>{profile.product_type}</span></li>
                            <li>Number of Employees: <span>{profile.employee_count}</span></li>
                            {/* <li>Interest: <span></span><i className="fa fa-pencil" data-toggle="modal"></i></li> MISSING FIELD API */}
                            <li className="profile-section-description">
                                <p><span>Business Details: </span> {profile.business_details}</p>
                            </li>
                        </ul>
                    </div>
                </div>
                <div className="profile-section profile-account-settings" id="profile-account-settings">
                    <div className="profile-section-title">
                        <p className="profile-section-header">Account Settings</p>
                    </div>
                    <div className="profile-section-subtitle">
                        <p>User Information</p>
                    </div>
                    <ul className="profile-section-info-list">
                        <li>Username: <span>{user.username}</span></li>
                        <li>Password: <span>*****</span><a className="fa fa-pencil" href="../change_password"></a></li>
                        <li>Blocklight Affiliate Code: <span>{affiliate}</span><button className="copy-btn" style={{cursor: 'pointer'}} onClick={() => this.handleShareClick()}>Share</button></li>
                    </ul>
                </div>
            </>
        )
    }
}



export default MyProfile;
