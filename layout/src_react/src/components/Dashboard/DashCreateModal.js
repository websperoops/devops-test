import React, { useState, useEffect } from 'react'
import ReactModal from 'react-modal';
import { csrf_token } from '../../functions/dashboard/dashFunctions';

function DashCreateModal(props) {

    const [showNewInput, setShowNewInput] = useState(false);
    const [showDeletedDashes, setShowDeletedDashes] = useState(false);
    const [name, setName] = useState(null);
    const [dashToRetrieve, setDashToRetrieve] = useState(null);
    const [retriveable, setRetriveable] = useState(null);

    useEffect(() => {
        setRetriveable(deletedDashes)
    }, [deletedDashes])

    const close = () => {
        setShowNewInput(false);
        setShowDeletedDashes(false);
        setName(null);
        setDashToRetrieve(null);

        props.close();
    }


    const createNewDash = async () => {
        const res = await fetch('../../newdash/', {
            method: 'POST',
            body: JSON.stringify(
                {
                    title: escape(name)
                }
            ),
            headers: {
                "X-CSRFToken": csrf_token,
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest'
            },
        });
        res.status === 200 && window.location.reload()

        console.log(res);
    }

    const retriveDash = async () => {
        if (dashToRetrieve !== null) {
            const res = await fetch('../../retrievedash/', {
                method: 'POST',
                body: JSON.stringify(
                    {
                        id: dashToRetrieve
                    }
                ),
                headers: {
                    "X-CSRFToken": csrf_token,
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'X-Requested-With': 'XMLHttpRequest'
                },
            });

            res.status === 200 && window.location.reload()
        }
    }

    const handleShowDeletedDashes = () => {
        setShowDeletedDashes(true)
        if (showNewInput) {
            setShowNewInput(false)
        }
    }

    const handleShowNewInput = () => {
        setShowNewInput(true);
        if (showDeletedDashes) {
            setShowDeletedDashes(false)
        }
    }


    return (
        <ReactModal onRequestClose={close} isOpen={props.show} shouldCloseOnEsc={true} ariaHideApp={false} className="modal-outer">
            <div className="modal-inner">
                <h3>What would you like to do?</h3>

                <div className="d-flex flex-row justify-content-center">
                    <button onClick={handleShowDeletedDashes} className="btn_long btn_orange">Retrieve Deleted</button>
                    <button onClick={handleShowNewInput} className="btn_long btn_clear">Create New</button>
                </div>
                {showNewInput && <div className=" mt-4 d-flex flex-column justify-content-center bg-light">
                    <div className="d-flex flex-column justify-content-center mt-3">
                        <label html="dash-name" style={{ fontSize: '20px' }}>Dashboard Title</label>
                        <input id="dash-name" className="mx-auto" type="text" onChange={e => setName(e.target.value)} style={{ width: '300px', borderRadius: '10px', border: '1px solid #ddd', textAlign: 'center' }} />
                    </div>
                    <div className="d-flex flex-row justify-content-center">
                        <button onClick={createNewDash} className="btn_orange">Create!</button>
                        <button onClick={close} className="btn_clear">Cancel</button>
                    </div>
                </div>}
                {showDeletedDashes &&
                    <div className="d-flex flex-column justify-content-center bg-light">
                        <label className="mt-2" ><h3>Retrievable Dashboards</h3></label>
                        <select className="text-center mx-auto mt-3" style={{ width: '200px' }} onChange={(e) => setDashToRetrieve(e.target.value)}>
                            <option value={null}>--- Select Dashboard ---</option>
                            {retriveable.map(dash => <option key={dash.id} value={dash.id}>{unescape(dash.title)}</option>)}
                        </select>
                        <div className="d-flex flex-row justify-content-center">
                            <button onClick={retriveDash} className="btn_orange">Retrieve</button>
                            <button onClick={close} className="btn_clear">Cancel</button>
                        </div>
                    </div>
                }
            </div>
        </ReactModal>
    )
}

export default DashCreateModal;