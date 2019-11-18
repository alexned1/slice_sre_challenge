require 'sinatra'
require 'sinatra/json'

configure { set :server, :puma }

class App < Sinatra::Base
  get '/sres' do
    json sres: ['bob', 'linda', 'tina', 'gene', 'louise']
  end

  get '/health' do
    json health: true, metrics: {requestLatency: rand, dbLatency: rand, cacheLatency: rand}
  end
end
