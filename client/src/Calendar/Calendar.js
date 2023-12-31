import React from 'react'
import FullCalendar from '@fullcalendar/react'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import INITIAL_EVENTS from "../assets/Events.json"

export default class Calendar extends React.Component {
  render() {
    return (
      <div className='calendar-container'>
        {this.renderSidebar()}
        <div className='calendar-container-main'>
          <FullCalendar
            plugins={[dayGridPlugin, timeGridPlugin]}
            headerToolbar={{
              left: 'prev,next today',
              center: 'title',
              right: 'timeGridWeek,timeGridDay'
            }}
            initialView='timeGridWeek'
            selectable={true}
            selectMirror={true}
            dayMaxEvents={true}
            weekends={true}
            initialEvents={INITIAL_EVENTS} 
            eventContent={renderEventContent} 
            eventClick={this.handleEventClick}
            eventsSet={this.handleEvents}
          />
        </div>
      </div>
    )
  }

  renderSidebar() {
    return (
      <div className='calendar-container-sidebar'>
        <div className='calendar-container-sidebar-section'>
          <h2>Instructions</h2>
          <ul>
            <li>View this almanac to note auspicious times</li>
            <li>Green represents good times, red represents bad times</li>
          </ul>
        </div>
        <div className='calendar-container-sidebar-section'>
          <h2>Legend</h2>
          <ul>
            <li>RK: Rahu Kalam</li>
            <li>YM: Yama Gandam</li>
            <li>GK: Gulika Kalam</li>
            <li>AJ: Abhijit Muhurta</li>
            <li>DM: Durmuhurtham</li>
            <li>V: Varjyam</li>
            <li>AK: Amrit Kalam</li>
          </ul>
        </div>
        <div className='calendar-container-sidebar-section'>
          <h2>Panchang Calendar</h2>
          <ul>
            <li>Download calendar <a className='download-button' onClick={this.handleDownload}>here</a> </li>
            <li>Times imported from <a target="_blank" href="https://mypanchang.com/">myPanchang</a> </li>
          </ul>
        </div>
      </div>
    )
  }

  handleEventClick = (clickInfo) => {
    alert(clickInfo.event.title);
  }

  handleEvents = (events) => {
    this.setState({
      currentEvents: events
    })
  }

  handleDownload = () => {
    const fileUrl = process.env.PUBLIC_URL + '/ics/Panchang 1.0.ics';
    window.open(fileUrl, '_blank');
  }
}

function renderEventContent(eventInfo) {
  return (
    <>
      <i>{eventInfo.timeText}</i>
      <br />
      <b>{eventInfo.event.title}</b>
    </>
  )
}