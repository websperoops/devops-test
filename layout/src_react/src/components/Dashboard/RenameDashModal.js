import React, { useState, useEffect } from 'react'
import ReactModal from 'react-modal';

function renameDashModal(props) {
    const [name, setName] = useState();
    const handleRename = async () => {

        var path = rename_url +
            "?dash_id=" + props.dashId +
            "&new_title=" + encodeURIComponent(name);
        const res = await fetch(path);
        window.location.reload()
    }

    useEffect(() => {
        setName(props.currentName)
    }, [props])

    const close = () => props.close();
    return (
        <ReactModal ariaHideApp={false} onRequestClose={close} shouldCloseOnEsc={true} isOpen={props.show} className="modal-outer">
            <div className="modal-inner">
                <h3 className="mb-3">Rename Dashboard</h3>

                <input className="text-center" type="text" value={decodeURIComponent(name)} onChange={e => setName(escape(e.target.value))} placeholder="New Name" style={{ border: '1px solid #ddd', borderRadius: '10px', width: '300px' }} />
                <div className="d-flex flex-row justify-content-center">
                    <button className="btn_orange" onClick={handleRename}>Rename!</button>
                    <button onClick={close} className="btn_clear">Cancel</button>
                </div>

            </div>
        </ReactModal>
    )
}

export default renameDashModal;