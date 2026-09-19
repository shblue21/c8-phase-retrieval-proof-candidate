(* Mathematical input used for the separate Wolfram tool verification.
   Only the final assignment/Print wrapper is added for file-based execution. *)
ClearAll["Global`*"];
p={1+I t+t^3+4I t^5+t^12/2-I t^13/2,t^2+I t^3/2-t^5+t^10-I t^11/2-t^13,t^4+I t^5+t^8/2-I t^9/2+t^11/2-2t^12,t^6-2I t^7,t^8+I t^9+t^11+4I t^13,t^10+I t^11/2-t^13,t^12+I t^13,t^14};
x=Table[Symbol["x"<>ToString[j]],{j,7}];y=Table[Symbol["y"<>ToString[j]],{j,7}];r=Table[Symbol["r"<>ToString[j]],{j,7}];a=Table[Symbol["a"<>ToString[j]],{j,7}];
run[ii_,start_,last_]:=Module[{v,h,pol,eq,co,j,k,subs={},vals},v=p[[ii+1]]+Sum[(x[[j]]+I y[[j]])p[[j+1]],{j,ii+1,7}];h=Sum[(r[[j]]+I a[[j]])p[[j+1]],{j,start,7}];pol=Expand[ComplexExpand[h Conjugate[v]+Conjugate[h]v]];Do[k=2ii+2j;eq=Expand[Coefficient[pol,t,k]/.subs];co=Coefficient[eq,r[[j]]];If[co===0,Return["ZERO_REAL_PIVOT"]];subs=Append[subs,r[[j]]->Expand[-(eq-co r[[j]])/co]];eq=Expand[Coefficient[pol,t,k+1]/.subs];co=Coefficient[eq,a[[j]]];If[co=!=0,subs=Append[subs,a[[j]]->Expand[-(eq-co a[[j]])/co]]],{j,start,last}];Table[Expand[Coefficient[pol,t,k]/.subs],{k,0,28}]];
z00=run[0,1,4];z0=run[0,4,7];z1=run[1,5,7];z2=run[2,4,6];z22=run[2,6,7];z4=run[4,6,7];
rp=x1^2+2(y1-2)^2+8;tp=-2x1 x3-4y1 y3-2x2;sp=-1-x1^2-y1^2-6x3^2-2y3^2-x2^2-y2^2;
checks={Expand[z00[[10]]-a2(5x1^2/6+5y1^2-4y1+10)]===0,Expand[z0[[18]]-(rp(a6-a4 x2)+2a4 tp)/2]===0,Expand[z0[[22]]-2a4 sp-tp(a6-a4 x2)]===0,Expand[rp z0[[22]]-2tp z0[[18]]-2a4(rp sp-tp^2)]===0,Expand[z1[[22]]+2a5(1+x2^2+y2^2+10x3^2+2y3^2)]===0,Expand[z2[[18]]+a4(30x3^2+5y3^2-4y3+10)]===0,Expand[z22[[22]]+2a6(1+6x3^2+2y3^2)]===0,Expand[z4[[26]]-a6(x5^2+2(y5-2)^2+8)/2]===0};
missing=And@@Flatten[Table[Expand[Coefficient[Expand[ComplexExpand[p[[j]]Conjugate[p[[k]]]]],t,d]]===0,{j,8},{k,8},{d,{1,5,13}}]];
result=<|"MissingProductCoefficients"->missing,"EightGateIdentities"->checks,"AllPass"->(missing&&And@@checks)|>;
Print[result];
