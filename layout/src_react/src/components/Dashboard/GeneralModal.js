import React from 'react'
import "./dashMainPage.css";

class GeneralModal extends React.Component {
    chartAction = () => {
        const { selected_id } = this.props;
        if (this.props.action === 'Delete') {
            window.$(`#${selected_id}_container`).remove(); //remove widget from dom using jquery
        }

        fetch(`${this.props.path}${selected_id}`).then(res => console.log(res))
        this.props.toggleModal();    //Close modal after you delete it
        // location.reload();
    }

    render() {
        return (
            <div className="modal" style={{ display: this.props.m === `${this.props.name}` ? 'block' : 'none', background: 'rgba(0, 0, 0, 0.5)' }}>
                <div className="vertical-alignment-helper">
                    <div className="modal-dialog modal-lg vertical-align-center">
                        <div className="modal-content theme-body" id="deleteChartModal_content">
                            <div className="modal-header deleteModal-header theme-text">
                                <h3>Are you sure you want to {this.props.action} this chart?</h3>
                            </div>
                            <div className="modal-body">

                                <div className="row justify-content-around">
                                    <div className="col-xs-3 delete-btn-div">
                                        <button onClick={this.chartAction} id="deleteChart" className="btn-block btn_orange">Yes</button>
                                    </div>
                                    <div className="col-xs-3 delete-btn-div">
                                        <button id="dontDeleteChart" className="btn-block btn_clear" onClick={() => this.props.toggleModal()}>No</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

export default GeneralModal;