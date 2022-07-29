import React, { useContext } from 'react'
import { SocialData } from './SocialContainer'

function PostModal() {
    const { showPostModal, closePostModal, activatePostModal } = useContext(SocialData);

    return (
        <div style={{ display: 'none' }} className="social-modal-container" onClick={closePostModal}>
            <div onClick={showPostModal} className="social-modal"> {/*So the modal doesnt close when we click on an item*/}
                <h3>Create A New Post</h3>
                <div className="inner-social-modal">
                    <p>Start by selecting a social network</p>

                    <div className="inner-social-sites">
                        <ul>
                            <li className="fa fa-facebook fa-3x"></li>
                            <li className="fa fa-instagram fa-3x"></li>

                        </ul>
                    </div>
                </div>
            </div>
        </div>
    )
}
export default PostModal