import axios from 'axios';
import { createClient } from '@supabase/supabase-js'
import * as dotenv from 'dotenv';

dotenv.config();
const supabaseKey = process.env.SUPABASE_KEY || '';
const supabaseUrl = process.env.SUPABASE_URL || '';
const supabase = createClient(supabaseUrl, supabaseKey);


interface Event {
  id: number;
  date_start: string;
  full_name: string;
  date_end: string;
}

let tok:string;

const postData = {
  client_id: '',
  client_secret: '',
  grant_type: 'client_credentials'
};

const url = 'https://apps.leader-id.ru/api/v1/events/search?paginationPage=1&paginationSize=15&sort=date&dateFrom=2023-07-28&dateTo=2023-08-03&participationFormat=person&placeIds[]=3942';

axios.post('https://apps.leader-id.ru/api/v1/oauth/token', postData)
  .then(response => {
    tok = response.data.access_token;
    (async () => {
      const events = await getEvents().then(
        events => insertEvents(events)
      );
    })();
  })
  .catch(error => {
    console.error(error);
  });


async function getEvents(): Promise<Event[]> {
  console.log(tok);
  const config = {
    headers: {
      'Authorization': 'Bearer '+ tok
    },
  };
  const response = await axios.get(url, config);
   const events: Event[] = response.data.items.map((event: any) => (
  {
     id: event.id,
     date_start: event.date_start,
     full_name: event.full_name,
     date_end: event.date_end,
   }
  ));
  console.log(events);
  return events;
}

async function insertEvents(events: Event[]) {
  try {
    await supabase.from('Event').insert(events);
} catch(error){
  console.error(error);
  }
}
    
  

