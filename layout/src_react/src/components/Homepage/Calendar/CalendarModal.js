import React, { useState } from 'react';
import { Alert } from 'react-bootstrap'
import ReactModal from 'react-modal';
import StartEndDate from './StartEndDate';
import './calendar.css';

const CalendarModal = ({ showModal, closeModal, selectStartDate, selectEndDate, onSumbitDate, validDateRange }) => {
  return (
    <ReactModal
      ariaHideApp={false}
      onRequestClose={closeModal}
      className="calendar-modal-outer"
      isOpen={showModal}
      shouldCloseOnEsc={true}
      shouldCloseOnOverlayClick={true}
    >
      <div className="calendar-modal-inner">
        <div className='calendar-title'>Date Range</div>
        <StartEndDate selectStartDate={selectStartDate} selectEndDate={selectEndDate}/>

        <div style={{marginTop:'20px'}}>
          <button className='calendar-btn calendar-submit-btn' onClick={onSumbitDate}>Submit</button>
          <button className='calendar-btn calendar-cancel-btn' onClick={closeModal}>Cancel</button>
        </div>

        {
          !validDateRange && <Alert className='mt-3 mb-0' variant={'danger'} style={{width: '300px', margin: 'auto'}}>Please select a valid date range.</Alert>
        }
      </div>
    </ReactModal>
  );
};

export default CalendarModal;
