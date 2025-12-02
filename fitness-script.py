import requests
import pandas as pd
from datetime import datetime
import os 
from dotenv import load_dotenv

load_dotenv()


class StravaETL:
    def __init__(self):
        self.client_id = os.getenv('STRAVA_CLIENT_ID')
        self.client_secret = os.getenv('STRAVA_CLIENT_SECRET')
        self.refresh_token = os.getenv('STRAVA_REFRESH_TOKEN')
        self.access_token = None

    def get_access_token(self):
        print("Getting fresh access token...")
        auth_url = "https://www.strava.com/oauth/token"  # FIXED: removed extra 's'
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token'
    }
        
    
        try:
            response = requests.post(auth_url, data=payload)  # POST, not GET
            response.raise_for_status()
            self.access_token = response.json()['access_token']
            print("✓ Access token obtained")
            return self.access_token
        except Exception as e:
            print(f"✗ Error getting access token: {e}")
            return None
        
    def fetch_activities(self, limit=200):
        """Fetch recent activities from Strava"""
        if not self.access_token:
            self.get_access_token()

        print(f"DEBUG: Using access token: {self.access_token[:10] if self.access_token else 'NONE'}...")
        
        print(f"Fetching last {limit} activities from Strava...")
        url = "https://www.strava.com/api/v3/athlete/activities"
        headers = {'Authorization': f'Bearer {self.access_token}'}
        params = {'per_page': limit}

        print(f"DEBUG: Request URL: {url}")
        print(f"DEBUG: Headers: {headers}")
        
        try:
            response = requests.get(url, headers=headers, params=params)
            print(f"DEBUG: Response status: {response.status_code}")
            print(f"DEBUG: Response body: {response.text[:200]}")
            response.raise_for_status()
            activities = response.json()
            print(f"✓ Retrieved {len(activities)} activities")
            return activities
        except Exception as e:
            print(f"✗ Error fetching activities: {e}")
            return []
        
    def process_activities(self,activities):
        #turning raw data into data frames, pythons excel sheets
        print("Processing activity data ...")
        data = []

        for activity in activities:
            pace = None
            pace_km = None
            if activity['type'] == 'Run' and activity['distance'] > 0:
                #calculate pace per mile
                pace = (activity['moving_time'] / 60) / (activity['distance'] / 1609.34)
            
            data.append({
                'date': activity['start_date'][:10],
                'activity_type': activity['type'],
                'name': activity['name'],
                'distance_miles': round(activity['distance'] / 1609.34, 2),
                'distance_km': round(activity['distance'] /1000, 2),
                'duration_minutes': round(activity['moving_time'] /60, 1),
                'elevation_feet': round(activity['total_elevation_gain'] * 3.28084,0),
                'calories': activity.get('calories',0),
                'average_heartrate': round(activity.get('average_heartrate', 0), 0),
                'max_heartrate': round(activity.get('max_heartrate', 0), 0),
                'average_speed_mph': round(activity['average_speed'] * 2.23694, 2),
                'pace_min_per_mile': round(pace,2) if pace else None, 
                'pace_min_per_km': round(pace_km,2) if pace_km else None,
                'kudos_count': activity.get('kudos_count', 0),
                'day_of_week': pd.to_datetime(activity['start_date'][:10]).strftime('%A'),
                'month': pd.to_datetime(activity['start_date'][:10]).strftime('%B'),
                'year': pd.to_datetime(activity['start_date'][:10]).year
            })
            
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date', ascending=False)

        print(f"Processed {len(df)} activities")
        return df
        
    def export_to_csv(self,df,filename='strava_data.csv'):
        #export DataFrame to CSV for PowerBi
        df.to_csv(filename, index=False)
        print(f"Exported to {filename}")
        return filename
    
    def print_summary(self, df):
        #print summary
        print("\n" + "="*50)
        print("SUMMARY STATISTICS")
        print("="*50)
        print(f"Total activities: {len(df)}")
        print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
        print(f"Total distance: {df['distance_miles'].sum():.1f} miles")
        print(f"Total time: {df['duration_minutes'].sum():.0f} minutes ({df['duration_minutes'].sum()/60:.1f} hours)")
        
        print(f"\nActivities by type:")
        print(df['activity_type'].value_counts())

        print(f"\nBreakdown by Activity Type:")
        for activity_type in df['activity_type'].unique():
            activities = df[df['activity_type'] == activity_type]
            total_distance = activities['distance_km'].sum()
            total_time = activities['duration_minutes'].sum()
    
            print(f"\n{activity_type}:")
            print(f"  Count: {len(activities)}")
            print(f"  Total distance: {total_distance:.1f} km")
            print(f"  Total time: {total_time:.0f} minutes ({total_time/60:.1f} hours)")
    
            # Calculate pace only for activities with distance
            if activity_type in ['Run', 'Ride', 'Walk'] and total_distance > 0:
                avg_pace = activities['pace_min_per_km'].mean()
                print(f"  Avg pace: {avg_pace:.2f} min/km")

            
        print("="*50 + "\n")

    def run(self):
        """Execute full ETL pipeline"""
        print("\n Starting Strava ETL Pipeline\n")
        
        # Fetch data
        activities = self.fetch_activities()
        
        if not activities:
            print("No activities found or error occurred")
            return None
        
        # Process data
        df = self.process_activities(activities)
        
        # Export
        self.export_to_csv(df)
        
        # Summary
        self.print_summary(df)
        
        return df


if __name__ == "__main__":
    etl = StravaETL()
    df = etl.run()    
