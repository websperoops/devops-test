import React from 'react'
import './integrations.css';

function AddIntegrationServiceBlock(props) {
    return (
        <div onClick={props.ToggleIntegrationModal} className="integration_block integration_add_block">
            <p style={{ marginBottom: '0' }}>Add New <i className="fa fa-plus"></i></p>
        </div>
    )
}

export default AddIntegrationServiceBlock;