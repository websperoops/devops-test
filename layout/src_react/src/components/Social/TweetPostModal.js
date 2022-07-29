import React, { useContext, useState } from 'react'
import ReactModal from 'react-modal'
import { SocialData } from './SocialContainer'
import { csrf_token } from '../../functions/dashboard/dashFunctions'

function TweetPostModal(props) {
    const [status, setStatus] = useState('')
    const updateStatus = async () => {
        if (status.length > 0) {
            const res = await fetch('/dashboards/social/new_tweet', {
                headers: {
                    "X-CSRFToken": csrf_token,
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                method: 'POST',
                body: JSON.stringify({
                    'new_post': encodeURIComponent(status)
                })
            })


            const json = await res.json()
            setStatus('')
            closePostModal()
        }

    }
    const { showPostModal, closePostModal, activatePostModal } = useContext(SocialData);
    return (
        <ReactModal onRequestClose={closePostModal} isOpen={showPostModal} shouldCloseOnEsc={true} ariaHideApp={false} className="modal-outer" shouldCloseOnOverlayClick={true}>
            <div className="modal-inner">

                <div className="d-flex flex-column">
                    <label htmlFor="post">Post New Tweet <i style={{ color: '#1da1f2' }} className="fa fa-twitter"></i></label>
                    <textarea style={{ resize: 'none', height: '100px' }} maxLength="240" onChange={e => setStatus(e.target.value)} className="form-control bg-light border-0 text-dark mt-3" id="post">
                    </textarea>
                </div>
                <p className="text-right mr-1" style={{ fontSize: '12px', color: '#ef7b14' }}>{status.length}/240</p >
                <div>
                    <input type="button" onClick={updateStatus} className="btn_orange" value="post" />
                    <input onClick={closePostModal} type="button" className="btn_clear" value="cancel" />
                </div>

            </div>
        </ReactModal >
    )
}
export default TweetPostModal