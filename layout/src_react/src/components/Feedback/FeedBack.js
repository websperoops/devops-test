import React, { useState } from 'react'
import { csrf_token } from '../../functions/dashboard/dashFunctions'
import './feedback.css';

const Feedback = () => {

    const [message, setMessage] = useState()
    const [topic, setTopic] = useState('overall_design_andor_functionality')
    const [status, setStatus] = useState()

    const onSubmit = async () => {
        const res = await fetch('/dashboards/feedback/', {
            method: 'POST',
            body: JSON.stringify(
                {
                    topic: topic,
                    description: message
                }
            ),
            headers: {
                "X-CSRFToken": csrf_token,
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest'
            },
        });

        // console.log(res);
        // const json = await res.json()
        // setStatus(json.status)

        if(res.ok){
            window.location.href = '/dashboards/feedback_sent'
        } else {
            setStatus('failed')
        }
    }


    return (
        <section className="feedback" id="feedback">
            <div className="container">
                {status === 'failed' && <div className="alert alert-danger" role="alert">
                    Oh no! Your submission was unsuccessful. Please try again
                </div>}
                {status === 'success' && <div className="alert alart-success" role="alert">
                    Thank you! We successfully received your feedback.
            </div>}

                <div className="feedback-header dark-theme-text">
                    <h2>WE APPRECIATE YOUR FEEDBACK!</h2>
                </div>
                <div className="feedback-form-group" id="feedback_form" method="post" action="/dashboards/feedback/">
                    <input type="hidden" name="csrfmiddlewaretoken" value={csrf_token} />
                    <div className="feedback-topic">
                        <select name="topic" id="topic_select"
                            className="form-control" onChange={e => setTopic(e.target.value)}>
                            <option disabled defaultValue={true} value="default">Select a topic</option>
                            <option value="overall_design_andor_functionality">Feedback on overall app design and/or
                                functionality</option>
                            <option value="specific_existing_metric">Feedback on a specific existing metric</option>
                            <option value="request_new_metric">Request for a new metric</option>
                            <option value="request_new_integration">Request for a new integration</option>
                            <option value="error">Unexpected error</option>
                            <option value="other">Other</option>
                        </select>
                    </div>

                    <div className="feedback-desc dark-theme-input">
                        <textarea className="form-control" required name="description" rows="10" cols="30"
                            placeholder="Add details here" value={message} onChange={e => setMessage(e.target.value)}></textarea>
                    </div>

                    <div className="feedback-form-group submit-button">
                        <button className="feedback-submit-btn btn_long" onClick={onSubmit}>Submit</button>
                    </div>
                </div>
            </div>


        </section >
    )
}
export default Feedback;