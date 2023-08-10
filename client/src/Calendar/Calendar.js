import React from 'react'
import FullCalendar from '@fullcalendar/react'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import INITIAL_EVENTS from "../assets/Events.json"

export default class Calendar extends React.Component {
  render() {
    return (
      <div className='demo-app'>
        {this.renderSidebar()}
        <div className='demo-app-main'>
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
      <div className='demo-app-sidebar'>
        <div className='demo-app-sidebar-section'>
          <h2>Instructions</h2>
          <ul>
            <li>View this almanac to note auspicious times</li>
            <li>Green represents good times, red represents bad times</li>
          </ul>
        </div>
        <div className='demo-app-sidebar-section'>
          <h2>Panchang Calendar</h2>
          <ul>
            <li>View source code <a target="_blank" href="https://github.com/adityakeerthi/panchang-cal">here</a> </li>
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

function renderSidebarEvent(event) {
  return (
    <li key={event.id}>
      <i>{event.title}</i>
    </li>
  )
}
