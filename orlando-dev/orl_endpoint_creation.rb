Publisher.create! do |pub|
  pub.title = "OPD Reports"
  pub.endpoint = "http://orlando-citygram-api.azurewebsites.net/?service=police"
  pub.active = true
  pub.visible = true
  pub.city = "Orlando"
  pub.icon = "police-incidents.png"
  pub.state = "FL"
  pub.description = "Orlando police incident reports are added when the report has closed."
  pub.tags = ["orlando","orl","crime","police"]
end