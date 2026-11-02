#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/netanim-module.h"
#include "ns3/flow-monitor-module.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("FirstScriptExample");

int main (int argc, char *argv[])
{
  //MY ID: 24101230
  uint32_t packetSize = 2410;   // will change this accordingly [4 times] following the instructions
  CommandLine cmd (__FILE__);
  cmd.AddValue("packetSize", "Size of packet to send in bytes", packetSize);
  cmd.Parse (argc, argv);
  
  Time::SetResolution (Time::NS);
  LogComponentEnable ("UdpClient", LOG_LEVEL_INFO);
  LogComponentEnable ("UdpServer", LOG_LEVEL_INFO);

  NodeContainer nodes;
  nodes.Create (2);

  PointToPointHelper pointToPoint;
  pointToPoint.SetDeviceAttribute ("DataRate", StringValue ("5Mbps"));
  pointToPoint.SetChannelAttribute ("Delay", StringValue ("2ms"));

  NetDeviceContainer devices;
  devices = pointToPoint.Install (nodes);

  InternetStackHelper stack;
  stack.Install (nodes);

  Ipv4AddressHelper address;
  address.SetBase ("10.1.1.0", "255.255.255.0");

  Ipv4InterfaceContainer interfaces = address.Assign (devices);

  UdpServerHelper udpServer (9);

  ApplicationContainer serverApps = udpServer.Install (nodes.Get (1));
  serverApps.Start (Seconds (1.0));
  serverApps.Stop (Seconds (10.0));

  UdpClientHelper udpClient (interfaces.GetAddress (1), 9);
  udpClient.SetAttribute ("MaxPackets", UintegerValue (1));
  udpClient.SetAttribute ("Interval", TimeValue (Seconds (1.0)));
  
  // Set your dynamic packet size here (Change this number for the home task)
  udpClient.SetAttribute ("PacketSize", UintegerValue (packetSize)); //MY ID: 24101230

  ApplicationContainer clientApps = udpClient.Install (nodes.Get (0));
  clientApps.Start (Seconds (2.0));
  clientApps.Stop (Seconds (10.0));

  // Task 9: Setup NetAnim Animation File
  AnimationInterface anim ("first.xml"); 

  // Task 10: Enable PCAP Tracing for Wireshark
  pointToPoint.EnablePcapAll ("first");

  // Task 11: Setup FlowMonitor
  FlowMonitorHelper flowHelper;
  Ptr<FlowMonitor> monitor = flowHelper.InstallAll ();

  Simulator::Stop (Seconds (20.0));
  Simulator::Run ();

  // Task 11: Process and Print Metrics
  monitor->CheckForLostPackets ();
  Ptr<Ipv4FlowClassifier> classifier = DynamicCast<Ipv4FlowClassifier> (flowHelper.GetClassifier ());
  std::map<FlowId, FlowMonitor::FlowStats> stats = monitor->GetFlowStats ();
  for (auto const& [id, stat] : stats) {
      Ipv4FlowClassifier::FiveTuple t = classifier->FindFlow (id);
      std::string proto = (t.protocol == 6) ? "TCP" : (t.protocol == 17) ? "UDP" : "Unknown";
      std::cout << "FlowID: " << id << " (" << proto << " "
                << t.sourceAddress << "/" << t.sourcePort << "-->"
                << t.destinationAddress << "/" << t.destinationPort << ")\n";
      std::cout << "  Tx Bytes: " << stat.txBytes << "\n";
      std::cout << "  Rx Bytes: " << stat.rxBytes << "\n";
      if (stat.rxPackets > 0) {
          std::cout << "  Mean Delay: " << stat.delaySum.GetSeconds()/stat.rxPackets << "s\n";
          std::cout << "  Throughput: " << (stat.rxBytes * 8.0) / 18.0 << "bps\n";
      }
  }

  Simulator::Destroy ();
  return 0;
}
