function [ scanData, success ] = catchLaser( sckLaser )

response=char(receiveMessage(sckLaser,0.1,0.02,15));
nlIndices=find(response==10);
if length(nlIndices)<4
   display('failed to get laser scan');
   return
end
beginIndex = nlIndices(4)+1;
endIndex=nlIndices(end-1)-1;
scanData=sscanf(response(beginIndex:endIndex),['<lval f="%f" ang="%f" dist="%f"/>' char(10)]);
scanData=scanData(1:floor(length(scanData)/3)*3);
scanData=reshape(scanData,3,length(scanData)/3);

success=1;