const FRED_API_BASE = 'https://api.stlouisfed.org/fred';
const API_KEY = process.env.NEXT_PUBLIC_FRED_API_KEY;

export interface FredObservation {
  date: string;
  value: string;
}

export interface FredSeriesResponse {
  observations: FredObservation[];
}

export async function fetchFredSeries(
  seriesId: string,
  startDate?: string,
  endDate?: string
): Promise<FredObservation[]> {
  if (!API_KEY || API_KEY === 'your_fred_api_key_here') {
    console.warn('FRED API key not configured. Using mock data.');
    return [];
  }

  const params = new URLSearchParams({
    series_id: seriesId,
    api_key: API_KEY,
    file_type: 'json',
  });

  if (startDate) params.append('observation_start', startDate);
  if (endDate) params.append('observation_end', endDate);

  try {
    const response = await fetch(
      `${FRED_API_BASE}/series/observations?${params.toString()}`
    );

    if (!response.ok) {
      throw new Error(`FRED API error: ${response.status}`);
    }

    const data: FredSeriesResponse = await response.json();
    return data.observations.filter((obs) => obs.value !== '.');
  } catch (error) {
    console.error('Error fetching FRED data:', error);
    return [];
  }
}

export async function fetchCPIData() {
  const endDate = new Date().toISOString().split('T')[0];
  const startDate = new Date(Date.now() - 5 * 365 * 24 * 60 * 60 * 1000)
    .toISOString()
    .split('T')[0];

  // CPI for All Urban Consumers: All Items in U.S. City Average (CPIAUCSL)
  // Using growth rate: Consumer Price Index for All Urban Consumers: All Items (CPALTT01USM657N)
  const data = await fetchFredSeries('CPALTT01USM657N', startDate, endDate);

  return data.map((obs) => ({
    date: new Date(obs.date).toLocaleDateString('en-US', {
      month: 'short',
      year: 'numeric',
    }),
    value: parseFloat(obs.value),
  }));
}

export async function fetchUnemploymentData() {
  const endDate = new Date().toISOString().split('T')[0];
  const startDate = new Date(Date.now() - 5 * 365 * 24 * 60 * 60 * 1000)
    .toISOString()
    .split('T')[0];

  // Unemployment Rate (UNRATE)
  const data = await fetchFredSeries('UNRATE', startDate, endDate);

  return data.map((obs) => ({
    date: new Date(obs.date).toLocaleDateString('en-US', {
      month: 'short',
      year: 'numeric',
    }),
    value: parseFloat(obs.value),
  }));
}

export async function fetch10YearTreasuryData() {
  const endDate = new Date().toISOString().split('T')[0];
  const startDate = new Date(Date.now() - 5 * 365 * 24 * 60 * 60 * 1000)
    .toISOString()
    .split('T')[0];

  // 10-Year Treasury Constant Maturity Rate (GS10)
  const data = await fetchFredSeries('GS10', startDate, endDate);

  return data.map((obs) => ({
    date: new Date(obs.date).toLocaleDateString('en-US', {
      month: 'short',
      year: 'numeric',
    }),
    value: parseFloat(obs.value),
  }));
}

export async function fetch3MonthTreasuryData() {
  const endDate = new Date().toISOString().split('T')[0];
  const startDate = new Date(Date.now() - 5 * 365 * 24 * 60 * 60 * 1000)
    .toISOString()
    .split('T')[0];

  // 3-Month Treasury Bill Secondary Market Rate (TB3MS)
  const data = await fetchFredSeries('TB3MS', startDate, endDate);

  return data.map((obs) => ({
    date: new Date(obs.date).toLocaleDateString('en-US', {
      month: 'short',
      year: 'numeric',
    }),
    value: parseFloat(obs.value),
  }));
}
